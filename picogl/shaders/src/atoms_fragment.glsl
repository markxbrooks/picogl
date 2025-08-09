#version 330 core

in vec3 fragNormal;
in vec3 fragColor;
in vec3 fragPosition;

out vec4 outColor;

uniform vec3 lightPos = vec3(10.0, 10.0, 10.0);
uniform vec3 viewPos = vec3(0.0, 0.0, 5.0);

// Fog parameters
uniform float fogDensity = 0.05;
uniform float fogNear = 1.0;
uniform float fogFar = 20.0;

void main() {
    // Round point shape
    float diameter = length(gl_PointCoord - vec2(0.5));
    if (diameter > 0.5)
        discard;

    vec3 lightDir = normalize(lightPos - fragPosition);
    vec3 norm = normalize(fragNormal);

    float diff = max(dot(norm, lightDir), 0.0);
    float ambient = 0.3;

    vec3 litColor = fragColor * (ambient + diff);

    // Gamma correction
    vec3 gammaCorrected = pow(litColor, vec3(1.0 / 2.2));

    // Fog calculation (exponential)
    float dist = length(viewPos - fragPosition);
    float fogFactor = clamp(exp(-fogDensity * dist * dist), 0.0, 1.0);

    vec3 fogColor = vec3(0.9); // light gray fog
    //vec3 finalColor = mix(fogColor, gammaCorrected, fogFactor);
    vec3 finalColor = mix(fogColor, gammaCorrected, fogFactor);
    outColor = vec4(gammaCorrected, 1.0);
}
