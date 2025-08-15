#version 330 core

in vec3 fragmentColor;
in vec3 normal;
in vec3 fragPosition;  // We'll pass this from the vertex shader

out vec4 color;

uniform vec3 lightPos; // World-space light position

void main()
{
    // Normalize interpolated normal
    vec3 norm = normalize(normal);

    // Compute light direction
    vec3 lightDir = normalize(lightPos - fragPosition);

    // Diffuse factor (Lambertian shading)
    float diff = max(dot(norm, lightDir), 0.0);

    // Ambient + Diffuse
    vec3 ambient = 0.2 * fragmentColor;
    vec3 diffuse = diff * fragmentColor;

    color = vec4(ambient + diffuse, 1.0);

}
