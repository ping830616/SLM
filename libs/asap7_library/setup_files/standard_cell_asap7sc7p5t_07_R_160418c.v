module A2O1A1Ixp33_ASAP7_75t_R_v1(A1,A2,B,C,Y);
	input	A1,A2,B,C;
	output	Y;
	or(_n2,B,_n1);
	and(_n1,A1,A2);
	nand(Y,C,_n2);
endmodule

module A2O1A1Ixp33_ASAP7_75t_R_v2(A1,A2,B,C,Y);
	input	A1,A2,B,C;
	output	Y;
	or(_n2,B,_n1);
	and(_n1,A1,A2);
	nand(Y,C,_n2);
endmodule

module A2O1A1O1Ixp33_ASAP7_75t_R_v1(A1,A2,B,C,D,Y);
	input	A1,A2,B,C,D;
	output	Y;
	or(_n2,B,_n1);
	nor(Y,D,_n3);
	and(_n1,A1,A2);
	and(_n3,C,_n2);
endmodule

module A2O1A1O1Ixp33_ASAP7_75t_R_v2(A,B,C,D,E,Y);
	input	A,B,C,D,E;
	output	Y;
	or(_n2,C,_n1);
	nor(Y,E,_n3);
	and(_n1,A,B);
	and(_n3,D,_n2);
endmodule

module AND4x2_ASAP7_75t_R(A,B,C,D,Y);
	input	A,B,C,D;
	output	Y;
	and(Y,A,B,C,D);
endmodule

module AO21x2_ASAP7_75t_R(A1,A2,B,Y);
	input	A1,A2,B;
	output	Y;
	or(Y,B,_n1);
	and(_n1,A1,A2);
endmodule

module AO22x2_ASAP7_75t_R(A1,A2,B1,B2,Y);
	input	A1,A2,B1,B2;
	output	Y;
	or(Y,_n1,_n2);
	and(_n1,A1,A2);
	and(_n2,B1,B2);
endmodule

module AO31x2_ASAP7_75t_R(A1,A2,A3,B,Y);
	input	A1,A2,A3,B;
	output	Y;
	or(Y,B,_n1);
	and(_n1,A1,A2,A3);
endmodule

module AO32x2_ASAP7_75t_R(A1,A2,A3,B1,B2,Y);
	input	A1,A2,A3,B1,B2;
	output	Y;
	or(Y,_n1,_n2);
	and(_n2,B1,B2);
	and(_n1,A1,A2,A3);
endmodule

module AOI211xp5_ASAP7_75t_R(A1,A2,B,C,Y);
	input	A1,A2,B,C;
	output	Y;
	nor(Y,B,C,_n1);
	and(_n1,A1,A2);
endmodule

module AOI21_x2_ASAP7_75t_R(A1,A2,B,Y);
	input	A1,A2,B;
	output	Y;
	nor(Y,B,_n1);
	and(_n1,A1,A2);
endmodule

module AOI22xp33_ASAP7_75t_R(A1,A2,B1,B2,Y);
	input	A1,A2,B1,B2;
	output	Y;
	nor(Y,_n1,_n2);
	and(_n2,A1,A2);
	and(_n1,B1,B2);
endmodule

module AOI31xp67_ASAP7_75t_R(A1,A2,A3,B,Y);
	input	A1,A2,A3,B;
	output	Y;
	nor(Y,B,_n1);
	and(_n1,A1,A2,A3);
endmodule

module AOI322xp5_ASAP7_75t_R(A1,A2,A3,B1,B2,C1,C2,Y);
	input	A1,A2,A3,B1,B2,C1,C2;
	output	Y;
	nor(Y,_n1,_n2,_n3);
	and(_n3,B1,B2);
	and(_n2,C1,C2);
	and(_n1,A1,A2,A3);
endmodule

module AOI32xp33_ASAP7_75t_R(A1,A2,A3,B1,B2,Y);
	input	A1,A2,A3,B1,B2;
	output	Y;
	nor(Y,_n1,_n2);
	and(_n1,B1,B2);
	and(_n2,A1,A2,A3);
endmodule

module AOI333xp33_ASAP7_75t_R(A1,A2,A3,B1,B2,B3,C1,C2,C3,Y);
	input	A1,A2,A3,B1,B2,B3,C1,C2,C3;
	output	Y;
	nor(Y,_n1,_n2,_n3);
	and(_n2,A1,A2,A3);
	and(_n3,B1,B2,B3);
	and(_n1,C1,C2,C3);
endmodule

module BUFx10_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	buf(Y,A);
endmodule

module BUFx12_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	buf(Y,A);
endmodule

module BUFx12f_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	buf(Y,A);
endmodule

module BUFx4_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	buf(Y,A);
endmodule

module BUFx6f_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	buf(Y,A);
endmodule

module BUFx8_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	buf(Y,A);
endmodule

module DFFHQNx1_ASAP7_75t_R(CLK,D,QN);
	input	CLK,D;
	output reg QN;
	always @(posedge CLK)
	QN<=!D;
endmodule

module DFFHQNx2_ASAP7_75t_R(CLK,D,QN);
	input	CLK,D;
	output reg QN;
	//not(_n1,_n2);
	//mux(QN,CLK,_n2,QN);
	//imux(_n2,CLK,_n1,D);
	always @(posedge CLK)
	QN<=!D;
endmodule

module DFFHQNx3_ASAP7_75t_R(CLK,D,QN);
	input	CLK,D;
	output reg QN;
	//not(_n1,_n2);
	//mux(QN,CLK,_n2,QN);
	//imux(_n2,CLK,_n1,D);
	always @(posedge CLK)
	QN<=!D;
endmodule

module DFFHQNx4_ASAP7_75t_R(CLK,D,QN);
	input	CLK,D;
	output reg QN;
	//not(_n1,_n2);
	//mux(QN,CLK,_n2,QN);
	//imux(_n2,CLK,_n1,D);
	always @(posedge CLK)
	QN<=!D;
endmodule

module DFFLQNx1_ASAP7_75t_R(CLK,D,QN);
	input	CLK,D;
	output reg QN;
	//not(_n1,_n2);
	//mux(QN,CLK,QN,_n2);
	//imux(_n2,CLK,D,_n1);
	always @(negedge CLK)
	QN<=!D;
endmodule

module DFFLQNx2_ASAP7_75t_R(CLK,D,QN);
	input	CLK,D;
	output reg QN;
	//not(_n1,_n2);
	//mux(QN,CLK,QN,_n2);
	//imux(_n2,CLK,D,_n1);
    always @(negedge CLK)
	QN<=!D;
endmodule

module DFFLQNx3_ASAP7_75t_R(CLK,D,QN);
	input	CLK,D;
	output reg QN;
	//not(_n1,_n2);
	//mux(QN,CLK,QN,_n2);
	//imux(_n2,CLK,D,_n1);
	always @(negedge CLK)
	QN<=!D;

endmodule

module DFFLQNx4_ASAP7_75t_R(CLK,D,QN);
	input	CLK,D;
	output reg QN;
	//not(_n1,_n2);
	//mux(QN,CLK,QN,_n2);
	//imux(_n2,CLK,D,_n1);
	always @(negedge CLK)
	QN<=!D;

endmodule

module DHLx1_ASAP7_75t_R(CLK,D,Q);
	input	CLK,D;
	output	Q;
	mux(Q,CLK,D,Q);
endmodule

module DHLx2_ASAP7_75t_R(CLK,D,Q);
	input	CLK,D;
	output	Q;
	mux(Q,CLK,D,Q);
endmodule

module DHLx3_ASAP7_75t_R(CLK,D,Q);
	input	CLK,D;
	output	Q;
	trireg	_n1;
	not(Q,_n1);
	bufif1(_n1,_n1,CLK);
	notif1(_n1,D,CLK);
endmodule

module DLLx1_ASAP7_75t_R(CLK,D,Q);
	input	CLK,D;
	output	Q;
	mux(Q,CLK,Q,D);
endmodule

module DLLx2_ASAP7_75t_R(CLK,D,Q);
	input	CLK,D;
	output	Q;
	mux(Q,CLK,Q,D);
endmodule

module DLLx3_ASAP7_75t_R(CLK,D,Q);
	input	CLK,D;
	output	Q;
	mux(Q,CLK,Q,D);
endmodule

module HB1xp67_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	buf(Y,A);
endmodule

module HB2xp67_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	buf(Y,A);
endmodule

module HB3xp67_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	buf(Y,A);
endmodule

module HB4xp67_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	buf(Y,A);
endmodule

module ICGNx1_ASAP7_75t_R(CLK,EN,GCLKN,SE);
	input	CLK,EN,SE;
	output	GCLKN;
	not(_n1,CLK);
	or(_n3,EN,SE);
	nand(GCLKN,_n1,_n2);
	mux(_n2,CLK,_n3,_n2);
endmodule

module ICGNx2_ASAP7_75t_R(CLK,EN,GCLKN,SE);
	input	CLK,EN,SE;
	output	GCLKN;
	or(GCLKN,CLK,_n1);
	nor(_n2,EN,SE);
	mux(_n1,CLK,_n2,_n1);
endmodule

module ICGx2_ASAP7_75t_R(CLK,EN,GCLK,SE);
	input	CLK,EN,SE;
	output	GCLK;
	or(_n1,EN,SE);
	and(GCLK,CLK,_n2);
	mux(_n2,CLK,_n1,_n2);
endmodule

module ICGx3_ASAP7_75t_R(CLK,EN,GCLK,SE);
	input	CLK,EN,SE;
	output	GCLK;
	or(_n2,EN,SE);
	and(GCLK,CLK,_n1);
	mux(_n1,CLK,_n2,_n1);
endmodule

module INVx11_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	not(Y,A);
endmodule

module INVx13_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	not(Y,A);
endmodule

module INVx1_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	not(Y,A);
endmodule

module INVx2_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	not(Y,A);
endmodule

module INVx3_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	not(Y,A);
endmodule

module INVx4_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	not(Y,A);
endmodule

module INVx5_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	not(Y,A);
endmodule

module INVx6_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	not(Y,A);
endmodule

module INVx8_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	not(Y,A);
endmodule

module INVxp33_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	not(Y,A);
endmodule

module INVxp67_ASAP7_75t_R(A,Y);
	input	A;
	output	Y;
	not(Y,A);
endmodule

module MAJIxp5_ASAP7_75t_R(A,B,C,Y);
	input	A,B,C;
	output	Y;
	imaj(Y,A,B,C);
endmodule

module NAND2x1_ASAP7_75t_R(A,B,Y);
	input	A,B;
	output	Y;
	nand(Y,A,B);
endmodule

module NAND2xp33_ASAP7_75t_R(A,B,Y);
	input	A,B;
	output	Y;
	nand(Y,A,B);
endmodule

module NAND2xp5_ASAP7_75t_R(A,B,Y);
	input	A,B;
	output	Y;
	nand(Y,A,B);
endmodule

module NAND2xp67_ASAP7_75t_R(A,B,Y);
	input	A,B;
	output	Y;
	nand(Y,A,B);
endmodule

module NAND3x1_ASAP7_75t_R(A,B,C,Y);
	input	A,B,C;
	output	Y;
	nand(Y,A,B,C);
endmodule

module NAND4xp25_ASAP7_75t_R(A,B,C,D,Y);
	input	A,B,C,D;
	output	Y;
	nand(Y,A,B,C,D);
endmodule

module NAND5xp2_ASAP7_75t_R(A,B,C,D,E,Y);
	input	A,B,C,D,E;
	output	Y;
	nand(Y,A,B,C,D,E);
endmodule

module NOR2x1_ASAP7_75t_R(A,B,Y);
	input	A,B;
	output	Y;
	nor(Y,A,B);
endmodule

module NOR2xp33_ASAP7_75t_R(A,B,Y);
	input	A,B;
	output	Y;
	nor(Y,A,B);
endmodule

module NOR2xp67_ASAP7_75t_R(A,B,Y);
	input	A,B;
	output	Y;
	nor(Y,A,B);
endmodule

module NOR3x1_ASAP7_75t_R(A,B,C,Y);
	input	A,B,C;
	output	Y;
	nor(Y,A,B,C);
endmodule

module NOR4xp25_ASAP7_75t_R(A,B,C,D,Y);
	input	A,B,C,D;
	output	Y;
	nor(Y,A,B,C,D);
endmodule

module NOR5xp2_ASAP7_75t_R(A,B,C,D,E,Y);
	input	A,B,C,D,E;
	output	Y;
	nor(Y,A,B,C,D,E);
endmodule

module O2A1Ixp5_ASAP7_75t_R(A1,A2,B,C,Y);
	input	A1,A2,B,C;
	output	Y;
	or(_n1,A1,A2);
	nor(Y,C,_n2);
	and(_n2,B,_n1);
endmodule

module OA21x2_ASAP7_75t_R(A1,A2,B,Y);
	input	A1,A2,B;
	output	Y;
	or(_n1,A1,A2);
	and(Y,B,_n1);
endmodule

module OA22x2_ASAP7_75t_R(A1,A2,B1,B2,Y);
	input	A1,A2,B1,B2;
	output	Y;
	or(_n2,A1,A2);
	or(_n1,B1,B2);
	and(Y,_n1,_n2);
endmodule

module OAI21xp5_ASAP7_75t_R_v1(A1,A2,B,Y);
	input	A1,A2,B;
	output	Y;
	or(_n1,A1,A2);
	nand(Y,B,_n1);
endmodule

module OAI21xp5_ASAP7_75t_R_v2(A1,A2,B,Y);
	input	A1,A2,B;
	output	Y;
	or(_n1,A1,A2);
	nand(Y,B,_n1);
endmodule

module OAI22xp5_ASAP7_75t_R(A1,A2,B1,B2,Y);
	input	A1,A2,B1,B2;
	output	Y;
	or(_n1,A1,A2);
	or(_n2,B1,B2);
	nand(Y,_n1,_n2);
endmodule

module OAI31xp67_ASAP7_75t_R(A1,A2,A3,B,Y);
	input	A1,A2,A3,B;
	output	Y;
	or(_n1,A1,A2,A3);
	nand(Y,B,_n1);
endmodule

module OAI32xp33_ASAP7_75t_R(A1,A2,A3,B1,B2,Y);
	input	A1,A2,A3,B1,B2;
	output	Y;
	or(_n1,B1,B2);
	or(_n2,A1,A2,A3);
	nand(Y,_n1,_n2);
endmodule

module SDFHx1_ASAP7_75t_R(CLK,D,QN,SE,SI);
	input	CLK,D,SE,SI;
	output reg QN;
	//mux(QN,CLK,_n1,QN);
	//mux(_n1,CLK,_n1,_n2);
	imux(_n2,SE,SI,D);
	always @(posedge CLK)
	QN<=_n2;


endmodule

module SDFHx3_ASAP7_75t_R(CLK,D,QN,SE,SI);
	input	CLK,D,SE,SI;
	output reg QN;
	//mux(QN,CLK,_n2,QN);
	//mux(_n2,CLK,_n2,_n1);
	imux(_n1,SE,SI,D);
	always @(posedge CLK)
	QN<=_n1;
endmodule

module SDFHx4_ASAP7_75t_R(CLK,D,QN,SE,SI);
	input	CLK,D,SE,SI;
	output reg QN;
	//mux(QN,CLK,_n2,QN);
	//mux(_n2,CLK,_n2,_n1);
	imux(_n1,SE,SI,D);
	always @(posedge CLK)
	QN<=_n1;
endmodule

module SDFLx1_ASAP7_75t_R(CLK,D,QN,SE,SI);
	input	CLK,D,SE,SI;
	output reg QN;
	//mux(QN,CLK,QN,_n2);
	//mux(_n2,CLK,_n1,_n2);
	imux(_n1,SE,SI,D);
	always @(negedge CLK)
	QN<=_n1;
endmodule

module XNOR2xp5_ASAP7_75t_R_v1(A,B,Y);
	input	A,B;
	output	Y;
	xnor(Y,A,B);
endmodule

module XNOR2xp5_ASAP7_75t_R_v2(A,B,Y);
	input	A,B;
	output	Y;
	xnor(Y,A,B);
endmodule

module XOR2x1_ASAP7_75t_R(A,B,Y);
	input	A,B;
	output	Y;
	xor(Y,A,B);
endmodule

module XOR2xp5_ASAP7_75t_R_v1(A,B,Y);
	input	A,B;
	output	Y;
	xor(Y,A,B);
endmodule

module XOR2xp5_ASAP7_75t_R_v2(A,B,Y);
	input	A,B;
	output	Y;
	xor(Y,A,B);
endmodule

primitive mux(Y,S,A,B);
	output	Y;
	input	S,A,B;
	table	1 1 ? : 1;
		1 0 ? : 0;
		0 ? 1 : 1;
		0 ? 0 : 0;
		? 1 1 : 1;
		? 0 0 : 0;
	endtable
endprimitive

primitive imux(Y,S,A,B);
	output	Y;
	input	S,A,B;
	table	1 1 ? : 0;
		1 0 ? : 1;
		0 ? 1 : 0;
		0 ? 0 : 1;
		? 1 1 : 0;
		? 0 0 : 1;
	endtable
endprimitive

primitive imaj(Y,A,B,C);
	output	Y;
	input	A,B,C;
	table	1 1 ? : 0;
		1 ? 1 : 0;
		? 1 1 : 0;
		0 0 ? : 1;
		0 ? 0 : 1;
		? 0 0 : 1;
	endtable
endprimitive

