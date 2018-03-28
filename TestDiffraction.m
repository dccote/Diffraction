%% Test Class Definition
classdef TestDiffraction < matlab.unittest.TestCase
    
    %% Test Method Block
    methods (Test)
        
        %% Test Function
        function testATest(testCase)      
            %% Exercise function under test
            % act = the value from the function under test
            testCase.verifyEqual(2+3,5);
        end
    end
end