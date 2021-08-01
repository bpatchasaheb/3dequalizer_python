#
# 3DE4.script.name:		Bake post filtered buffer curves
#
# 3DE4.script.version:		v1.3
#
# 3DE4.script.gui:Curve Editor::Edit
#
# 3DE4.script.comment: Bakes translation and rotation keyframes, so that any Post Filter smoothing, etc. is baked from the Filtered Curves, to the Raw curves. After bake, automatically sets Post Filter to Off. May then need Euler Flipping Filter applied.
#
#
# Patcha Saheb(patchasaheb@gmail.com)
#


from vl_sdv import*

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frames = tde4.getCameraNoFrames(cam)
pg_type = tde4.getPGroupType(pg)
currentFrame = tde4.getCurrentFrame(cam)
if pg_type == "CAMERA":
	for i in range(1,frames+1):
		tde4.setCurrentFrame(cam,i)
		frame = tde4.getCurrentFrame(cam)	
		pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
		rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
		scale = tde4.getPGroupScale3D(pg)
		#focal = tde4.getCameraFocalLength(cam,frame)
		tde4.setPGroupPosition3D(pg,cam,frame,pos.list())
		tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
		tde4.setPGroupScale3D(pg,scale)
		#tde4.setCameraFocalLength(cam,frame,focal)
	pf_mode  = tde4.getPGroupPostfilterMode(pg)
	tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
	tde4.filterPGroup(pg,cam)
	tde4.setPGroupPostfilterMode(pg,pf_mode)
if pg_type == "OBJECT":
	pg = tde4.getCurrentPGroup()
	for i_pg in tde4.getPGroupList():
		if tde4.getPGroupType(i_pg) == "CAMERA":
			id_cpg = i_pg
			break
	id_opg = pg		
	for i in range(1,frames+1):
		tde4.setCurrentFrame(cam,i)
		frame = tde4.getCurrentFrame(cam)
		rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
		pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
		rot_pos_base = igl3d(rot_cpg,pos_cpg)

		rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,cam,frame))
		pos_opg_global = vec3d(tde4.getPGroupPosition3D(id_opg,cam,frame))
		scale = tde4.getPGroupScale3D(pg)

		rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_global).invert() * rot_pos_base
		tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
		tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())
		tde4.setPGroupScale3D(pg,scale)
	pf_mode  = tde4.getPGroupPostfilterMode(pg)
	tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
	tde4.filterPGroup(pg,cam)
	tde4.setPGroupPostfilterMode(pg,pf_mode)
#only change from public, returns to parked frame
tde4.setCurrentFrame(cam,currentFrame)
