clear all
MP = [];
MP_MATRIX = [];

xyz_0 = circle(0, 0).pos;
for t = 0:0.05:20
    SP = circle(t, 0);
    SP.pos = SP.pos - xyz_0;
    MP = [MP, SP];
    SP_VEC = [SP.pos; SP.vel; SP.acc];
    MP_MATRIX=[MP_MATRIX, SP_VEC];
end

csvwrite('MP.csv', MP_MATRIX)
save MP.mat MP_MATRIX