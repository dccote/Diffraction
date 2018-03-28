classdef TestDiffraction < matlab.unittest.TestCase
    methods (Test)
        
        function testATest(testCase)      
            testCase.verifyEqual(2+3,5);
        end
    
        function testWhatIsAMesh(testCase)
            [x,y]=meshgrid(-2:1:2, -2:1:2);
            testCase.verifyEqual([ -2 -1 0 1 2; -2 -1 0 1 2; -2 -1 0 1 2; -2 -1 0 1 2;-2 -1 0 1 2 ], x);
            testCase.verifyEqual([ -2 -1 0 1 2; -2 -1 0 1 2; -2 -1 0 1 2; -2 -1 0 1 2;-2 -1 0 1 2 ]', y);
        end
        
        function testSquareGeneration(testCase)      
            [x,y]=meshgrid(-2:1:2, -2:1:2);
            image = generateCenteredSquare(x,y, 1);
            
            testCase.verifyEqual(logical([ 0 0 0 0 0;0 0 0 0 0; 0 0 1 0 0; 0 0 0 0 0; 0 0 0 0 0]), image);
        end
        
        function testBigSquareGeneration(testCase)      
            [x,y]=meshgrid(-2:1:2, -2:1:2);
            image = generateCenteredSquare(x,y, 3);
            
            testCase.verifyEqual(logical([ 0 0 0 0 0;0 1 1 1 0; 0 1 1 1 0; 0 1 1 1 0; 0 0 0 0 0]), image);
        end
        
        
        function testCircleGeneration(testCase)      
            [x,y]=meshgrid(-2:1:2, -2:1:2);
            image = generateCenteredCircle(x,y, 1);
            
            testCase.verifyEqual(logical([ 0 0 0 0 0;0 0 0 0 0; 0 0 1 0 0; 0 0 0 0 0; 0 0 0 0 0]), image);
        end
        
        function testBigCircleGeneration(testCase)      
            [x,y]=meshgrid(-2:1:2, -2:1:2);
            image = generateCenteredCircle(x,y, 2);
            
            testCase.verifyEqual(logical([ 0 0 0 0 0;0 1 1 1 0; 0 1 1 1 0; 0 1 1 1 0; 0 0 0 0 0]), image);
        end
        
        function testVeryBigCircleGeneration(testCase)
            [x,y]=meshgrid(-3:1:3, -3:1:3);
            image = generateCenteredCircle(x,y, 2.5);
            
            testCase.verifyEqual(logical([ 0 0 0 0 0 0 0; 0 0 1 1 1 0 0 ; 0 1 1 1 1 1 0; 0 1 1 1 1 1 0; 0 1 1 1 1 1 0; 0 0 1 1 1 0 0; 0 0 0 0 0 0 0]), image);
        end
    
    end
end