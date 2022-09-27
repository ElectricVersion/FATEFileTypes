meta:
  id: sms
  title: SMS File
  file-extension: SMS
  endian: le
  encoding: UTF-8
seq:
  - id: sms_file
    type: sms_file
types:
  sms_file:
    seq:
      - id: file_header
        type: file_header
      - id: material_section
        type: material_section
      - id: mesh_section
        type: mesh_section
      - id: bone_section
        type: bone_section
  file_header:
    seq:
      - id: version_string
        type: str
        terminator: 0
      - id: model_scale
        type: f4
      - id: mesh_count
        type: s4
      - id: vertex_count
        type: s4
      - id: tag_count
        type: s4
      - id: material_count
        type: s4
      - id: texture_count
        type: s4
  material_section:
    seq:
      - id: texture_defs
        type: texture_def
        repeat: expr
        repeat-expr: _root.sms_file.file_header.texture_count
      - id: material_defs
        type: material_def
        repeat: expr
        repeat-expr: _root.sms_file.file_header.material_count
    types:
      texture_def:
        seq:
          - id: texture_name
            type: str
            terminator: 0
          - id: texture_id
            type: s4
      material_def:
        seq:
          - id: material_name
            type: str
            terminator: 0
          - id: material_id
            type: s4
          - id: double_sided
            type: s4
          - id: is_collideable
            type: s4
          - id: is_visible
            type: s4
          - id: data_id
            type: s4
          - id: has_color_key
            type: s4
          - id: color_key
            type: rgb_s2
            if: has_color_key == 1
          - id: has_shifting_behavior
            type: s4
          - id: uv_shift
            type: uv_f4
            if: has_shifting_behavior == 1
          - id: has_flipbook_behavior
            type: s4
          - id: flipbook_behavior
            type: flipbook_behavior
            if: has_flipbook_behavior == 1
          - id: has_shifting_behavior2
            type: s4
          - id: uv_shift2
            type: uv_f4
            if: has_shifting_behavior2 == 1
          - id: has_flipbook_behavior2
            type: s4
          - id: flipbook_behavior2
            type: flipbook_behavior
            if: has_flipbook_behavior2 == 1
          - id: render_last
            type: s4
          - id: render_first
            type: s4
          - id: diffuse_color
            type: rgb_s2
          - id: ambient_color
            type: rgb_s2
          - id: specular_color
            type: rgb_s2
          - id: emissive_color
            type: rgb_s2
          - id: shininess
            type: f4
          - id: shininess_strength
            type: f4
          - id: diffuse_map_id
            type: s4
          - id: opacity_map_id
            type: s4
          - id: reflection_map_id
            type: s4
          - id: illumination_map_id
            type: s4
          - id: bump_map_id
            type: s4
          - id: sphere_map_id
            type: s4
          - id: multiply_map_id
            type: s4
        types:
          flipbook_behavior:
            seq:
              - id: w_frame_count
                type: s2
              - id: h_frame_count
                type: s2
              - id: time
                type: f4
  mesh_section:
    seq:
      - id: tag_defs
        type: tag_def
        repeat: expr
        repeat-expr: _parent.file_header.tag_count
      - id: mesh_defs
        type: mesh_def
        repeat: expr
        repeat-expr: _parent.file_header.mesh_count
    types:
      tag_def:
        seq:
          - id: tag_name
            type: str
            terminator: 0
          - id: has_user_data
            type: s2
          - id: user_data
            type: str
            terminator: 0
            if: has_user_data > 0
      mesh_def:
        seq:
          - id: mesh_name
            type: str
            size: 68
          - id: texture_count
            type: u4
          - id: vertex_count
            type: u4
          - id: triangle_count
            type: u4
          - id: triangle_start
            type: u4
          - id: header_size
            type: u4
          - id: uv_start
            type: u4
          - id: vertex_start
            type: u4
          - id: mesh_size
            type: u4
          - id: triangles
            type: tri_def
            repeat: expr
            repeat-expr: triangle_count
          - id: uvs
            type: uv_f4
            repeat: expr
            repeat-expr: vertex_count
          - id: vertices
            type: vertex_def
            repeat: expr
            repeat-expr: vertex_count
  bone_section:
    seq:
      - id: bone_count
        type: u4
      - id: bone_defs
        type: bone_def
        repeat: expr
        repeat-expr: bone_count
    types:
      bone_def:
        seq:
          - id: bone_name
            type: str
            terminator: 0
          - id: bone_parent
            type: s4
          - id: matrix
            type: bone_matrix
  rgb_s2:
    seq:
      - id: r
        type: s2
      - id: g
        type: s2
      - id: b
        type: s2
  uv_f4:
    seq:
      - id: u
        type: f4
      - id: v
        type: f4
  bone_matrix:
    types:
      vec3_f4:
        seq:
          - id: x
            type: f4
          - id: y
            type: f4
          - id: z
            type: f4
      vec3_s2:
        seq:
          - id: x
            type: s2
          - id: y
            type: s2
          - id: z
            type: s2
    seq:
      - id: translation
        type: vec3_f4
      - id: row0
        type: vec3_s2
      - id: row1
        type: vec3_s2
      - id: row2
        type: vec3_s2
  tri_def:
    seq:
      - id: vert_a
        type: u4
      - id: vert_b
        type: u4
      - id: vert_c
        type: u4
      - id: material
        type: u4
  vertex_def:
    types:
      bone_rel:
        seq:
          - id: bone_idx
            type: u4
          - id: x
            type: f4
          - id: y
            type: f4
          - id: z
            type: f4
          - id: au
            type: u1
          - id: av
            type: u1
          - id: weight
            type: f4
    seq:
      - id: bone_count
        type: u4
      - id: bone_relations
        type: bone_rel
        repeat: expr
        repeat-expr: bone_count
  addr:
    instances:
      position:
        value: _root._io.pos
    seq:
      - size: 0
        if: position == 0