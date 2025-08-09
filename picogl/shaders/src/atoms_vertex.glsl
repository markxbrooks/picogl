#version 330 core

// Input vertex data
layout(location = 0) in vec3 vertexPosition_modelspace;
layout(location = 1) in vec3 vertexColor;
layout(location = 2) in vec3 normal;

// Outputs to fragment shader
out vec3 fragNormal;
out vec3 fragColor;
out vec3 fragPosition;

// Uniforms
uniform mat4 mvp;
uniform mat4 model;
uniform float zoom_scale;

void main() {
    vec4 worldPos = model * vec4(vertexPosition_modelspace, 1.0);
    fragPosition = worldPos.xyz;

    // Transform normal to world space
    fragNormal = mat3(transpose(inverse(model))) * normal;
    fragColor = vertexColor;

    gl_Position = mvp * vec4(vertexPosition_modelspace, 1.0);

    float baseSize = 20.0;
    float adjusted_scale = pow(zoom_scale, 0.35);
    gl_PointSize = baseSize * adjusted_scale;
}
