function image = generateCenteredSquare(xMesh, yMesh, squareLength)

image = abs(xMesh) < squareLength/2 & abs(yMesh) < squareLength/2;

end