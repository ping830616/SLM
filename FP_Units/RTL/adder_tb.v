// Code your testbench here
// or browse Examples
module tb_adder16;
  reg rst, en, out_ready, clk;
  reg [15:0] a, b, z;
  int count;
  
  adder16 add (.clk(clk), .en(en), .rst(rst), .a(a), .b(b), .z(z), .output_ready(out_ready));
  
  always #5 clk = ~clk;
  
  initial begin
    en = 1;
    count = 0;
    clk = 0;
    
    a = 16'h3c00; //1
    b = 16'h4000; //2 , Res: 3 = 4200
    
    #10 
    a = 0; //0
    b = 0; //0 , Res : 0
    
    #10
    a = 16'h482c; //8.34
    b = 16'h3380; //0.2344, Res: 8.58 = 484a
     
    #10
    a = 0;
    b = 0;
    
    #10
    a = 16'h41f4; //2.977 
    b = 16'h3d6d; //1.356, Res: 4.332 = 4455
    
    #10
    a = 0;
    b = 0;
    
    #10
    a = 16'h5624; //98.25
    b = 16'h57b5; //123.3, Res: 221.5 = 5aec
    
    #10
    a = 0;
    b = 0;
    
    #10
    a = 16'h3759; //0.4592
    b = 16'h62d1; //872.5, Res : 873.0 = 62d2
    
    #10
    a = 0;
    b = 0;
    
    #10
    b = 16'h0000; //0
    a = 16'hbcf4; //-1.238 : bcf4
    
    #10
    a = 0;
    b = 0;
    
    #10
    a = 16'hbc00; //-1
    b = 16'hbcf4; //-1.238, Res: -2.238 : c07a
    
    #10
    a = 0;
    b = 0;
    
    #10
    a = 16'heac8; //-3472
    b = 16'hbcf4; //-1.238, Res: -3474 : eac9
    
     #10
    a = 0;
    b = 0;
    
    #10
    a = 16'hda40; //-200
    b = 16'hbcf4; //-1.238, Res: -201.2 : da4a
    
    #10
    a = 0;
    b = 0;
    
    #10
    a = 16'hb383; //-0.2347
    b = 16'hbcf4; //-1.238, Res: -1.473 bde4
    
    #10
    a = 0;
    b = 0;
    
    #10 
    a = 16'h3587; //0.3455
    b = 16'hbcf9; //-1.243, Res: -0.8975, bb2e
    
    
    #10
    a = 0;
    b = 0;
    
    #10 
    a = 16'h3d62; //1.346
	  b = 16'hbcf9; //-1.243, Res: 0.10254, 2e90
    #10
    a = 0;
    b = 0;
    
    #10
    a = 16'h3afc; //-0.873
    b = 16'hbafc; //0.873, Res: 0
    
	  #10
    a = 0;
    b = 0;
    
    #10
    a = 16'h3587; //0.3455
    b = 16'hb587; //-0.3455, Res: 0
    

    
    #100 $finish;
  end
  
  always@(posedge clk) begin
    count = count++;
    $display("COUNT:%d, out_ready:%b, A:%h , B:%h, Z:%h",count, out_ready, a, b,z);
  end
  
endmodule
