function [desired_state] = circle(t, qn)
% CIRCLE trajectory generator for a circle

% =================== Your code goes here ===================
% You have to set the pos, vel, acc, yaw and yawdot variables

% disp(t);
% r = 5;
% NTurns = 1;
% MaxAng = NTurns*2*pi; % Number of turns in helix
% c = 2.5/MaxAng; % Determines end z point
% omega = 0.6; % rad/s
% MaxTime = MaxAng/omega;
% a3 = -2*MaxAng/(omega*MaxTime^3);
% a2 = -3*MaxAng/(2*omega*MaxTime);
% theta = omega*(a3*t^3+a2*t^2);

r = 2;
NTurns = 2;
MaxAng = NTurns*2*pi; % Number of turns in helix
c = 2.5/MaxAng; % Determines end z point
omega = 0.6; % rad/s
MaxTime = MaxAng/omega;
a3 = -2*MaxAng/(omega*MaxTime^3);
a2 = -(3/2)*a3*MaxTime;
theta = omega*(a3*t^3+a2*t^2);
x = r*cos(theta);
y = r*sin(theta);
z = c*theta;

% theta = t;%0:StepSize:MaxAng;
% syms theta x y z
if(t>MaxTime)
    pos = [5; 0; 2.5];
    vel = [0; 0; 0];
    acc = [0; 0; 0];
    yaw = 0;
    yawdot = 0;
    desired_state.pos = pos(:);
    desired_state.vel = vel(:);
    desired_state.acc = acc(:);
    desired_state.yaw = yaw;
    desired_state.yawdot = yawdot;
else
    x = r*cos(theta);
    y = r*sin(theta);
    z = c*theta;
    
    % xdot = omega*r*-sin(theta);
    % ydot = omega*r*cos(theta);
    % 
    % xddot = omega*r*r*-cos(theta);
    % yddot = omega*r*r*-sin(theta);
    % 
    xdot = -omega*r*sin(omega*(a3*t^3 + a2*t^2))*(3*a3*t^2 + 2*a2*t);
    ydot = omega*r*cos(omega*(a3*t^3 + a2*t^2))*(3*a3*t^2 + 2*a2*t);
    
    zdot = c*omega*(3*a3*t^2 + 2*a2*t);
    
    xddot = - omega*r*sin(omega*(a3*t^3 + a2*t^2))*(2*a2 + 6*a3*t) - omega^2*r*cos(omega*(a3*t^3 + a2*t^2))*(3*a3*t^2 + 2*a2*t)^2;
    yddot = omega*r*cos(omega*(a3*t^3 + a2*t^2))*(2*a2 + 6*a3*t) - omega^2*r*sin(omega*(a3*t^3 + a2*t^2))*(3*a3*t^2 + 2*a2*t)^2;
    
    zddot = c*omega*(2*a2 + 6*a3*t);
    yaw = 0;
    yawdot = 0;
    pos = [x;y;z];
    vel = [xdot;ydot;zdot];
    acc = [xddot;yddot;zddot];
end
% =================== Your code ends here ===================

desired_state.pos = pos(:);
desired_state.vel = vel(:);
desired_state.acc = acc(:);
desired_state.yaw = yaw;
desired_state.yawdot = yawdot;

end
