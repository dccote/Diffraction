function image = generateCenteredCircle(xMesh, yMesh, radius)

image = xMesh.*xMesh + yMesh.*yMesh < radius*radius;

end