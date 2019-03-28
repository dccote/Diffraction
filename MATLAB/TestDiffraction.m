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

        function testSineConstruction(testCase)
            xMax = 100;
            deltaX = 0.1
            x = [-xMax:deltaX:xMax];
            sinX = sin(2*pi*x)+sin(pi*x); 
            
            testCase.verifyLessThan(sinX(1), 1e-7);       
            testCase.verifyLessThan(sinX(1+10), 1e-7);
            testCase.verifyLessThan(sinX(200), 1e-7);
        end

        function testZeroFreqencyIsFirst(testCase)
            xMax = 100;
            deltaX = 0.1
            x = [-xMax:deltaX:xMax];
            constant = repmat(1,2*xMax/deltaX);
            spectrum = fft(constant);

            testCase.verifyGreaterThan(abs(spectrum(1)), 1);       
            for i = 2:length(x)-1
                testCase.verifyLessThan(abs(spectrum(i)), 1e-2);       
            end
        end

        function testDiscretePeak(testCase)
            xMax = 100;
            deltaX = 0.1
            x = [-xMax:deltaX:xMax];
            sinX = sin(2*pi*x); 
            
            spectrum = fft(sinX); % Expect peak at 1 2 3 and 4

            fMax = 1.0/(deltaX);
            deltaF = 1/(2*xMax);
            
            expectedFreq1Pos = 1 + (1/deltaF); 
            expectedFreq1Neg = (length(x) + 1) + 1 - expectedFreq1Pos; 
            testCase.verifyGreaterThan(abs(spectrum(expectedFreq1Pos)), 900);       
            testCase.verifyGreaterThan(abs(spectrum(expectedFreq1Neg)), 900);       
        end
            
    
    end
end