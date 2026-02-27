module adder16(input clk,
						 input rst,
						 input en,
						 input [15:0] a,
						 input [15:0] b,
						 output [15:0] z,
						 output output_ready);

reg s_a, s_b, s_z;
// reg [9:0] e_a, e_b, e_z, e_min, diff;
reg [6:0] e_a, e_b, e_z, e_min, diff;
// reg [26:0] m_a, m_b;
reg [13:0] m_a, m_b;
// reg [23:0] m_z;
reg [10:0] m_z;
// reg [27:0] temp;
reg [14:0] temp;
reg guard, round, lonz;
//reg diff;
reg [15:0] Z, temp2;
reg out_ready;

// Still needs to be done
reg [4:0] diff2;
//reg [31:0] val32;
reg [15:0] val16;
reg [7:0] val8;
reg [3:0] val4;
//reg [3:0] state;

always@(posedge clk) begin		
	if(rst == 1) begin
		diff = 0;
		diff2 = 0;
		Z = 15'd0;
		out_ready = 0;
		temp = 0;
		//state <= enable;
	end
	else if (en == 0) begin
		out_ready = 0;
	end
	else if (en == 1) begin
		s_a = a[15];
		s_b = b[15];
		e_a = a[14:10] - 15;
		e_b = b[14:10] - 15;
		m_a[13] = 1;
		m_b[13] = 1;
		m_a [12:3]= a[9:0];
		m_b [12:3]= b[9:0];
		//These are the three round, lonz and guard bits for the mantissa
		m_a [2:0] = 3'd0;
		m_b [2:0] = 3'd0;

		//Either a or b is NaN
		if((e_a == 16 && m_a[12:0] != 0) || (e_b == 16 && m_b[12:0] != 0)) begin
			Z[15] = 1;
			Z[14:10] = 5'b11111;
			Z[9] = 1;
			Z[8:0] = 0;
			out_ready = 1;
		end

		//a is Inf
		else if(e_a == 16) begin
			//z is Inf
			Z[15] = s_a;
			Z[14:10] = 5'b11111;
			Z[9:0] = 0;
			out_ready = 1;
		end

		//b is Inf
		else if(e_b == 16) begin
			//z is Inf
			Z[15] = s_b;
			Z[14:10] = 5'b11111;
			Z[9:0] = 0;
			out_ready = 1;
		end

		//a and b are 0
		else if(($signed(e_a) == -15 && m_a[12:0] == 0) && ($signed(e_b) == -15 && m_b[12:0] == 0)) begin	   
			Z[15] = s_a & s_b;
			Z[14:10] = 0;
			Z[9:0] = 0;
			out_ready = 1;
			//state <= put_z;
		end

		//a is 0
		else if($signed(e_a) == -15 && m_a[12:0] == 0) begin	   
			Z[15] = s_b;
			Z[14:10] = e_b[4:0] + 15;
			Z[9:0] = m_b[12:3];
			out_ready = 1;
			//z[63:0] <= b[63:0];
			//state <= put_z;
		end

		//b is 0
		else if($signed(e_b) == -15 && m_b[12:0] == 0) begin	   
			Z[15] = s_a;
			Z[14:10] = e_a[4:0] + 15;
			Z[9:0] = m_a[12:3];
			out_ready = 1;
			//state <= put_z;
		end

		//a and b are equal in magnitude but have opposite signs
		else if(($signed(e_a) == $signed(e_b)) && (m_a == m_b) && (s_a != s_b)) begin
			Z[15] = 0;
			Z[14:10] = 0;
			Z[9:0] = 0;
			out_ready = 1;
		end

		else begin					
			//Align mantissas
			if($signed(e_a) > $signed(e_b)) begin
				diff = e_a - e_b;
				e_b = e_b + diff;
				m_b = m_b >> diff;
				m_b[0] = m_b[0] | m_b[1];
			end
			else if ($signed(e_a) < $signed(e_b)) begin
				diff = e_b - e_a;
				e_a = e_a + diff;
				m_a = m_a >> diff;
				m_a[0] = m_a[0] | m_a[1];
			end
			e_z = e_a;

			//If both sign bits are same
			if(s_a == s_b) begin
				temp = m_a + m_b;
				s_z = s_a;
			end
			else begin
				if(m_a >= m_b) begin
					temp = m_a - m_b;
					s_z = s_a;
				end
				else begin
					temp = m_b - m_a;
					s_z = s_b;
				end
			end

			//If temp overflows, carry out is 1
			if(temp[14] == 1) begin
				//Mantissa MSB carried forward
				m_z = temp[14:4];
				//Exponent incremented by 1
				e_z = e_z + 1;
				guard = temp[3];
				round = temp[2];
				lonz = temp[1] | temp[0];
			end
			//If no overflow, do not increment exponent, mantissa
			else begin
				m_z = temp[13:3];
				guard = temp[2];
				round = temp[1];
				lonz = temp[0];
				//m_z = m_z << 1;
				//e_z = e_z - 1;
				m_z[0] = guard;
			end

			//If MSB of manitssa + 1 (hidden bit) is 1
			if(m_z [10] == 0) begin
				temp2 [10:0] = m_z; //Transfer mantissa to temp2 
				temp2 [15:11] = 0;
				
				//
				if (temp2 == 0) begin 
					diff2 = 16;
				end
				else begin
					//diff2[6] = 1'b0;
					// diff2[5] = 1'b0;
					//val32 = diff2[5] ? temp2[31:0] : temp2[63:32];
					// diff2[4] = (temp2[31:16] == 16'b0);
					diff2[4] = 1'b0;
					// val16 = diff2[4] ? temp2[15:0] : temp2[31:16];
					// diff2[3] = (val16[15:8] == 8'b0);
					diff2[3] = (temp2[15:8] == 8'b0);
					// val8 = diff2[3] ? val16[7:0] : val16 [15:8];
					val8 = diff2[3] ? temp2[7:0] : temp2[15:8];
					diff2[2] = (val8[7:4] == 4'b0);
					val4 = diff2[2] ? val8[3:0] : val8[7:4];
					diff2[1] = (val4[3:2] == 2'b0);
					//val2 = diff2[1] ? val4[1:0] : val4[3:2];
    				diff2[0] = diff2[1] ? ~val4[1] : ~val4[3];
				end
				m_z = m_z << (diff2 - 5);
				e_z = e_z - (diff2 - 5);
			end

			//Verify this
			//Round overflow
			if(guard && (round | lonz | m_z[0])) begin
				m_z = m_z + 1;
				if(m_z == 11'd2047) begin
					e_z = e_z + 1;
				end
			end

			//Pack Output
			Z[9:0] = m_z [9:0];
			Z[14:10] = e_z[4:0] + 15;	
			Z[15] = s_z;
			if($signed(e_z) < -14) begin
				Z[15:0] = 0; 
			end
			if($signed(e_z) == -15 && m_z[10] == 0)
				Z[14:10] = 0;
			if ($signed(e_z) == -15 && m_z[10:0] == 11'h0)
			          Z[15] = 0; // -a + a = +0.
			if($signed(e_z) > 15) begin
				Z[9:0] = 0;
				Z[14:10] = 5'b11111;
				Z[15] = s_z;
			end
			out_ready = 1;	
		end
		//out_z <= Z;
		//out_ready <= o_r;
	end
end
assign z = Z;
assign output_ready = out_ready;
endmodule
