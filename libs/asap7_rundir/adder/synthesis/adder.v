
module adder (cout, a,b,sum,clk);

input clk;
input [1:0]a,b;
output reg [1:0] sum;

output reg cout;

always @(posedge clk)
begin 
	{cout,sum} <= a+b;
end
endmodule
