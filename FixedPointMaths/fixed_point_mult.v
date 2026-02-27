module fixed_mult #(
	//Parameterized values
	parameter Q = 15,
	parameter N = 32
	)
	(
	 input			[N-1:0]	in_multiplicand,
	 input			[N-1:0]	in_multiplier,
	 output			[N-1:0]	out_result,
	 output	reg				ovr
	 );
	 
	
	
	reg [2*N-1:0]	r_result;		
											
	reg [N-1:0]	r_RetVal;
	

	assign o_result = r_RetVal;	
	
	always @(in_multiplicand, in_multiplier)	begin						
		r_result <= in_multiplicand[N-2:0] * in_multiplier[N-2:0];	
																
		ovr <= 1'b0;															
		end
	
		
	always @(r_result) begin													
		r_RetVal[N-1] <= in_multiplicand[N-1] ^ in_multiplier[N-1];	
		r_RetVal[N-2:0] <= r_result[N-2+Q:Q];								
																						
		if (r_result[2*N-2:N-1+Q] > 0)										
			ovr <= 1'b1;
		end

endmodule