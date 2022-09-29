import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO

import json

if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))



class Sms(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self

    def _read(self):
        self.sms_file = Sms.SmsFile(self._io, self, self._root)
        self.sms_file._read()

    class UvF4(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.u = self._io.read_f4le()
            self.v = self._io.read_f4le()


    class VertexDef(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.bone_count = self._io.read_u4le()
            self.bone_relations = []
            for i in range(self.bone_count):
                _t_bone_relations = Sms.VertexDef.BoneRel(self._io, self, self._root)
                _t_bone_relations._read()
                self.bone_relations.append(_t_bone_relations)


        class BoneRel(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.bone_idx = self._io.read_u4le()
                self.x = self._io.read_f4le()
                self.y = self._io.read_f4le()
                self.z = self._io.read_f4le()
                self.au = self._io.read_u1()
                self.av = self._io.read_u1()
                self.weight = self._io.read_f4le()



    class SmsFile(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.file_header = Sms.FileHeader(self._io, self, self._root)
            self.file_header._read()
            self.material_section = Sms.MaterialSection(self._io, self, self._root)
            self.material_section._read()
            self.mesh_section = Sms.MeshSection(self._io, self, self._root)
            self.mesh_section._read()
            self.bone_section = Sms.BoneSection(self._io, self, self._root)
            self.bone_section._read()


    class BoneMatrix(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.translation = Sms.BoneMatrix.Vec3F4(self._io, self, self._root)
            self.translation._read()
            self.row0 = Sms.BoneMatrix.Vec3S2(self._io, self, self._root)
            self.row0._read()
            self.row1 = Sms.BoneMatrix.Vec3S2(self._io, self, self._root)
            self.row1._read()
            self.row2 = Sms.BoneMatrix.Vec3S2(self._io, self, self._root)
            self.row2._read()

        class Vec3F4(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.x = self._io.read_f4le()
                self.y = self._io.read_f4le()
                self.z = self._io.read_f4le()


        class Vec3S2(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.x = self._io.read_s2le()
                self.y = self._io.read_s2le()
                self.z = self._io.read_s2le()



    class RgbS2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.r = self._io.read_s2le()
            self.g = self._io.read_s2le()
            self.b = self._io.read_s2le()


    class Addr(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            if self.position == 0:
                self._unnamed0 = self._io.read_bytes(0)


        @property
        def position(self):
            if hasattr(self, '_m_position'):
                return self._m_position

            self._m_position = self._root._io.pos()
            return getattr(self, '_m_position', None)


    class MeshSection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.tag_defs = []
            for i in range(self._parent.file_header.tag_count):
                _t_tag_defs = Sms.MeshSection.TagDef(self._io, self, self._root)
                _t_tag_defs._read()
                self.tag_defs.append(_t_tag_defs)

            self.mesh_defs = []
            for i in range(self._parent.file_header.mesh_count):
                _t_mesh_defs = Sms.MeshSection.MeshDef(self._io, self, self._root)
                _t_mesh_defs._read()
                self.mesh_defs.append(_t_mesh_defs)


        class TagDef(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.tag_name = (self._io.read_bytes_term(0, False, True, True)).decode(u"UTF-8")
                self.has_user_data = self._io.read_s2le()
                if self.has_user_data > 0:
                    self.user_data = (self._io.read_bytes_term(0, False, True, True)).decode(u"UTF-8")



        class MeshDef(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.mesh_name = (self._io.read_bytes(68)).decode(u"UTF-8")
                self.texture_count = self._io.read_u4le()
                self.vertex_count = self._io.read_u4le()
                self.triangle_count = self._io.read_u4le()
                self.triangle_start = self._io.read_u4le()
                self.header_size = self._io.read_u4le()
                self.uv_start = self._io.read_u4le()
                self.vertex_start = self._io.read_u4le()
                self.mesh_size = self._io.read_u4le()
                self.triangles = []
                for i in range(self.triangle_count):
                    _t_triangles = Sms.TriDef(self._io, self, self._root)
                    _t_triangles._read()
                    self.triangles.append(_t_triangles)

                self.uvs = []
                for i in range(self.vertex_count):
                    _t_uvs = Sms.UvF4(self._io, self, self._root)
                    _t_uvs._read()
                    self.uvs.append(_t_uvs)

                self.vertices = []
                for i in range(self.vertex_count):
                    _t_vertices = Sms.VertexDef(self._io, self, self._root)
                    _t_vertices._read()
                    self.vertices.append(_t_vertices)




    class TriDef(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.vert_a = self._io.read_u4le()
            self.vert_b = self._io.read_u4le()
            self.vert_c = self._io.read_u4le()
            self.material = self._io.read_u4le()


    class FileHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.version_string = (self._io.read_bytes_term(0, False, True, True)).decode(u"UTF-8")
            self.model_scale = self._io.read_f4le()
            self.mesh_count = self._io.read_s4le()
            self.vertex_count = self._io.read_s4le()
            self.tag_count = self._io.read_s4le()
            self.material_count = self._io.read_s4le()
            self.texture_count = self._io.read_s4le()


    class BoneSection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.bone_count = self._io.read_u4le()
            self.bone_defs = []
            for i in range(self.bone_count):
                _t_bone_defs = Sms.BoneSection.BoneDef(self._io, self, self._root)
                _t_bone_defs._read()
                self.bone_defs.append(_t_bone_defs)


        class BoneDef(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.bone_name = (self._io.read_bytes_term(0, False, True, True)).decode(u"UTF-8")
                self.bone_parent = self._io.read_s4le()
                self.matrix = Sms.BoneMatrix(self._io, self, self._root)
                self.matrix._read()



    class MaterialSection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self

        def _read(self):
            self.texture_defs = []
            for i in range(self._root.sms_file.file_header.texture_count):
                _t_texture_defs = Sms.MaterialSection.TextureDef(self._io, self, self._root)
                _t_texture_defs._read()
                self.texture_defs.append(_t_texture_defs)

            self.material_defs = []
            for i in range(self._root.sms_file.file_header.material_count):
                _t_material_defs = Sms.MaterialSection.MaterialDef(self._io, self, self._root)
                _t_material_defs._read()
                self.material_defs.append(_t_material_defs)


        class TextureDef(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.texture_name = (self._io.read_bytes_term(0, False, True, True)).decode(u"UTF-8")
                self.texture_id = self._io.read_s4le()


        class MaterialDef(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self

            def _read(self):
                self.material_name = (self._io.read_bytes_term(0, False, True, True)).decode(u"UTF-8")
                self.material_id = self._io.read_s4le()
                self.double_sided = self._io.read_s4le()
                self.is_collideable = self._io.read_s4le()
                self.is_visible = self._io.read_s4le()
                self.data_id = self._io.read_s4le()
                self.has_color_key = self._io.read_s4le()
                if self.has_color_key == 1:
                    self.color_key = Sms.RgbS2(self._io, self, self._root)
                    self.color_key._read()

                self.has_shifting_behavior = self._io.read_s4le()
                if self.has_shifting_behavior == 1:
                    self.uv_shift = Sms.UvF4(self._io, self, self._root)
                    self.uv_shift._read()

                self.has_flipbook_behavior = self._io.read_s4le()
                if self.has_flipbook_behavior == 1:
                    self.flipbook_behavior = Sms.MaterialSection.MaterialDef.FlipbookBehavior(self._io, self, self._root)
                    self.flipbook_behavior._read()

                self.has_shifting_behavior2 = self._io.read_s4le()
                if self.has_shifting_behavior2 == 1:
                    self.uv_shift2 = Sms.UvF4(self._io, self, self._root)
                    self.uv_shift2._read()

                self.has_flipbook_behavior2 = self._io.read_s4le()
                if self.has_flipbook_behavior2 == 1:
                    self.flipbook_behavior2 = Sms.MaterialSection.MaterialDef.FlipbookBehavior(self._io, self, self._root)
                    self.flipbook_behavior2._read()

                self.render_last = self._io.read_s4le()
                self.render_first = self._io.read_s4le()
                self.diffuse_color = Sms.RgbS2(self._io, self, self._root)
                self.diffuse_color._read()
                self.ambient_color = Sms.RgbS2(self._io, self, self._root)
                self.ambient_color._read()
                self.specular_color = Sms.RgbS2(self._io, self, self._root)
                self.specular_color._read()
                self.emissive_color = Sms.RgbS2(self._io, self, self._root)
                self.emissive_color._read()
                self.shininess = self._io.read_f4le()
                self.shininess_strength = self._io.read_f4le()
                self.diffuse_map_id = self._io.read_s4le()
                self.opacity_map_id = self._io.read_s4le()
                self.reflection_map_id = self._io.read_s4le()
                self.illumination_map_id = self._io.read_s4le()
                self.bump_map_id = self._io.read_s4le()
                self.sphere_map_id = self._io.read_s4le()
                self.multiply_map_id = self._io.read_s4le()

            class FlipbookBehavior(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self

                def _read(self):
                    self.w_frame_count = self._io.read_s2le()
                    self.h_frame_count = self._io.read_s2le()
                    self.time = self._io.read_f4le()


with open("femaleupper.sms", "rb") as target_file:
    contents = KaitaiStream(target_file)
    parsed = Sms(_io=contents)
    parsed._read()

dont_parse = ["_io", "_parent", "_root"]

def make_dict(p_struct):
    out = vars(p_struct)
    for i in dont_parse:
        if i in out:
            del out[i]
    for i in out:
        if issubclass(type(out[i]), KaitaiStruct):
            out[i] = make_dict(out[i])
        elif type(out[i]) == list:
            for j in range(len(out[i])):
                out[i][j] = make_dict(out[i][j])
    return out
    
with open("femaleupper.json", "w") as target_file:
    json.dump(make_dict(parsed), target_file, indent=4)