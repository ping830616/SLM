module mult16(input clk,
	      input rst,
	      input en,
	      input [15:0] a,
	      input [15:0] b,
	      output [15:0] z,
		  output output_ready);

reg [23:0] temp_out;
reg [4:0] diff2;

reg s_a, s_b, s_z;
reg [6:0] e_a, e_b, e_z;
reg [10:0] m_a, m_b, m_z;
reg guard, round, lonz;
//reg [3:0] state;
reg [15:0] Z, temp2;
reg out_ready;

reg [15:0] val16;
reg [7:0] val8;
reg [3:0] val4;

always@(posedge clk)
begin

	if(rst == 1)
	begin
		Z = 16'd0;
		out_ready = 0;
	end
	else if(en == 0)
	begin
		out_ready = 0;
	end
	else if(en == 1)
	begin 

		s_a = a[15];
		s_b = b[15];
		e_a = a[14:10] - 15;
		e_b = b[14:10] - 15;
		m_a[9:0] = a[9:0];
		m_b[9:0] = b[9:0];
		m_a[10] = 1;
		m_b[10] = 1;

		//Either a or b is NaN
		if((e_a == 16 && m_a[9:0] != 0) || (e_b == 16 && m_b[9:0] != 0))
		begin
			Z[15] = 1;
			Z[14:10] = 5'b11111;
			Z[9] = 1;
			Z[8:0] = 0;
			out_ready = 1;
		end
		//a is Inf
		else if(e_a == 16)
		begin
			//b is 0; Inf * 0 = NaN
			if(($signed(e_b) == -15) && (m_b[9:0] == 0))
			begin
				Z[15] = 1;
				Z[14:10] = 5'b11111;
				Z[9] = 1;
				Z[8:0] = 0;
				out_ready = 1;
			end
			//z is Inf
			else
			begin
				Z[15] = s_a ^ s_b;
				Z[14:10] = 5'b11111;
				Z[9:0] = 0;
				out_ready = 1;
			end
		end
		//b is Inf
		else if(e_b == 16)
		begin
			//a is 0; Inf * 0 = NaN
			if(($signed(e_a) == -15) && (m_a[9:0] == 0))
			begin
				Z[15] = 1;
				Z[14:10] = 5'b11111;
				Z[9] = 1;
				Z[8:0] = 0;
				out_ready = 1;
			end
			//z is Inf
			else
			begin
				Z[15] = s_a ^ s_b;
				Z[14:10] = 8'hff;
				Z[8:0] = 0;
				out_ready = 1;
			end
		end
		//a is 0
		else if($signed(e_a) == -15 && m_a[9:0] == 0)  	
		begin	   
			Z[15] = s_a ^ s_b;
			Z[14:10] = 0;
			Z[9:0] = 0;
			out_ready = 1;
		end
		//b is 0
		else if($signed(e_b) == -15 && m_b[9:0] == 0)	
		begin	   
			Z[15] = s_a ^ s_b;
			Z[14:10] = 0;
			Z[9:0] = 0;
			out_ready = 1;
		end
		
		else
		begin
			s_z = s_a ^ s_b;
			e_z = e_a + e_b + 1;
			temp_out = m_a * m_b * 4;
			m_z = temp_out [23:13];
			guard = temp_out [12];
			round = temp_out [11];
			lonz = (temp_out[10:0] != 0);

			if(m_z[10] == 0)
			begin
				temp2 [10:0] = m_z[10:0];
				temp2 [15:11] = 0;
				if (temp2 == 0)
				begin 
					diff2 = 16;
				end
				else
				begin
			//		diff2[6] = 1'b0;
    			// diff2[5] = 1'b0;
    			//val32 = diff2[5] ? temp2[31:0] : temp2[63:32];
  		  		// diff2[4] = (temp2[31:16] == 16'b0);
    			diff2[4] = 1'b0;
				// val16 = diff2[4] ? temp2[15:0] : temp2[31:16];
    			// diff2[3] = (val16[15:8] == 8'b0);
				diff2[3] = (temp2[15:8] == 8'b0);
    			val8 = diff2[3] ? temp2[7:0] : temp2 [15:8];
    			diff2[2] = (val8[7:4] == 4'b0);
    			val4 = diff2[2] ? val8[3:0] : val8[7:4];
    			diff2[1] = (val4[3:2] == 2'b0);
					//val2 = diff2[1] ? val4[1:0] : val4[3:2];
    			diff2[0] = diff2[1] ? ~val4[1] : ~val4[3];
				end
				m_z = m_z << (diff2 - 5);
				e_z = e_z - (diff2 - 5);
			end
	
			if (guard && (round | lonz | m_z[0]))
			begin
				m_z = m_z + 1;
				if(m_z == 11'd4095)
				begin
					e_z = e_z + 1;
				end
			end

			//Pack Output
			Z[9:0] = m_z [9:0];
			Z[14:10] = e_z [4:0] + 15;	
			Z[15] = s_z;
			if($signed(e_z) < -14)
			begin
				Z[15:0] = 0; 
			end
			if($signed(e_z) == -14 && m_z[10] == 0)
			begin
				Z[14:10] = 0;
			end	
			if($signed(e_z) > 15)
			begin
				Z[9:0] = 0;
				Z[14:10] = 5'b11111;
				Z[15] = s_z;
			end
			out_ready = 1;		
		end
	end
end
assign z = Z;
assign output_ready = out_ready;
endmodule	


  
    
