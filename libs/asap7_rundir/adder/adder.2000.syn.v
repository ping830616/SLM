/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : S-2021.06-SP5-4
// Date      : Wed Jul  5 20:51:11 2023
/////////////////////////////////////////////////////////////


module adder ( cout, a, b, sum, clk );
  input [1:0] a;
  input [1:0] b;
  output [1:0] sum;
  input clk;
  output cout;
  wire   n4, n5, n6, n7, n8;

  DFFHQNx1_ASAP7_75t_R sum_reg_1_0 ( .D(n7), .CLK(clk), .QN(sum[1]) );
  DFFHQNx1_ASAP7_75t_R sum_reg_0_0 ( .D(n8), .CLK(clk), .QN(sum[0]) );
  DFFHQNx1_ASAP7_75t_R cout_reg ( .D(n6), .CLK(clk), .QN(cout) );
  XOR2xp5_ASAP7_75t_R U8 ( .A(a[1]), .B(b[1]), .Y(n4) );
  AND2x2_ASAP7_75t_R U9 ( .A(a[0]), .B(b[0]), .Y(n5) );
  AOI32xp33_ASAP7_75t_R U11 ( .A1(b[0]), .A2(n4), .A3(a[0]), .B1(b[1]), .B2(
        a[1]), .Y(n6) );
  XNOR2xp5_ASAP7_75t_R U12 ( .A(n5), .B(n4), .Y(n7) );
  XNOR2xp5_ASAP7_75t_R U13 ( .A(b[0]), .B(a[0]), .Y(n8) );
endmodule

