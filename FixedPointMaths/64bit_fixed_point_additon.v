module 64_bit_adder(addend1,addend2,sum);
input [63:0] addend1,addend2;
	output[63:0] sum;
	wire carry_out;
	wire [63:0] carry;
	genvar i;
	generate
		for(i=0;i<64;i=i+1)
			begin: generate_64_bit_adder
			if(i==0)
				half_adder f(addend1[0],addend2[0],sum[0],carry[0]);
			else
				full_adder f(addend1[i],addend2[i],carry[i-1],sum[i],carry[i]);
			end
		assign carryout = carry[63];
	endgenerate
endmodule

module half_adder(a,b,sum,c_out);
	input a,b;
	output sum,carry;
	assign s=x^y;
	assign cout=x&y;
endmodule

module full_adder(a,b,c_in,sum,c_out);
	input x,y,c_in;
	output sum,c_out;
	assign sum = (a^b)^c_in;
	assign c_out = (a&b) | (a&c_in) | (b&c_in);
endmodule