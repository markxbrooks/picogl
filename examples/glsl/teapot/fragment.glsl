#version 330 core

in vec3 fragmentColor;
in vec3 fragNormal;
in vec3 fragPosition;

out vec4 color;

uniform vec3 lightPos;
uniform vec3 viewPos;

void main() {
    vec3 norm = normalize(fragNormal);
    vec3 lightDir = normalize(lightPos - fragPosition);

    // Diffuse
    float diff = max(dot(norm, lightDir), 0.0);

    // Ambient and diffuse lighting
    vec3 ambient = 0.2 * fragmentColor;
    vec3 diffuse = diff * fragmentColor;

    color = vec4(ambient + diffuse, 1.0);
}
