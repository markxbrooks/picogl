#version 330 core
in vec3 frag_color;
out vec4 out_color;

void main() {
    out_color = vec4(frag_color, 1.0);
    //out_color = vec4(0.0, 1.0, 0.0, 1.0);  // Green
}
