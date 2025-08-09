#version 330 core
in vec3 fragNormal;
in vec3 fragColor;

out vec4 frag_output;

void main() {
    vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    float diff = max(dot(normalize(fragNormal), lightDir), 0.0);
    float ambient = 0.3; // tweak between 0.1–0.5
    vec3 color = pow(fragColor * (ambient + diff), vec3(1.0/2.2)); // gamma correction
    frag_output = vec4(color, 1.0);
}