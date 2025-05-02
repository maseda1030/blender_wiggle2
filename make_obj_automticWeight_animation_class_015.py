import os
import bpy
import math
import copy
import time
import inspect#関数名を出力するためだけのもの
#2024/10/9 
#print文はBlenderのメニューバーの Window > Toggle System Consoleを実行するとDOS窓が表示される

#make obj 円柱作成 Blender text ここでは日本語の入力はできないので、他で入力してコピペして
#Next here 10/14
#next code is 3 obj and 3 armatureBones.  so make Function objAndBones(location,gDepth,gCountBones)
def funcObjAndBones(mylocation,myDepth,myCountBones):
    #location=(0, 0, gDepth/2)
    loc=mylocation
    #円柱Vertices16，半径0.5ｍ、Depth6ｍ　座標：０，０，３ｍ（Depth6ｍ/2）
    #中心点をDepth6ｍ/2　半分Z軸を上げる
    # location=(0, 0, 3)#z is 3m , Depth is 6m, its half size.
    bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=0.5, depth=myDepth, enter_editmode=False,\
                                         align='WORLD', location=loc, scale=(1, 1, 1))
    #CTR+R bunkatsu 16 cuts
    #Start edit mode 
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut=
                {"number_cuts":16, "smoothness":0,\
                    "falloff":'INVERSE_SQUARE', "object_index":0, "edge_index":15,\
                    "mesh_select_mode_init":(True, False, False)},\
                        TRANSFORM_OT_edge_slide={"value":0, "single_side":False,\
                                "use_even":False, "flipped":False, \
                                "use_clamp":True, "mirror":True, "snap":False, \
                                "snap_elements":{'INCREMENT'}, "use_snap_project":False, \
                                "snap_target":'CLOSEST', "use_snap_self":True, \
                                "use_snap_edit":True, "use_snap_nonedit":True,\
                                "use_snap_selectable":False, "snap_point":(0, 0, 0),\
                                "correct_uv":True, "release_confirm":False, "use_accurate":False})
    bpy.ops.object.editmode_toggle()#from edit to OBJ mode 
    # end edit mode
    #add bone 1
    #ボーンのlocationのZ軸は原点に戻す必要がある。
    loc=(mylocation[0],mylocation[1],mylocation[2]-myDepth/2)
    bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=loc, \
                                scale=(1, 1, myDepth/myCountBones)) #6/4=1.5　Z軸スケールがなんかうまくいってない2024/10/15
    # Edit mode start
    bpy.ops.object.editmode_toggle()
    #add bone2 to (gCountBones-1)
    #ボーンの増加は、大きい親ボーンを分割処理してもいいのかも。試してみて。2024/10/15
    #E key EXTRUDE add child bone
    if myCountBones < 2:
        myCountBones=2
    #range(num) is 0 to num-1. exp: num=9 then 012345678 , its 9 counts. not exist [number9] .     
    for i in range(myCountBones):# range() is from 0 to (gcountBones-1),  total count is [gCountBOnes].
        if i >= myCountBones-1:
            break
        else:
            bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False},\
             TRANSFORM_OT_translate={"value":(0, 0, myDepth/myCountBones),\
              "orient_type":'GLOBAL',\
               "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)),\
                "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True),\
                 "mirror":False, "use_proportional_edit":False,\
                  "proportional_edit_falloff":'SMOOTH',\
                   "proportional_size":1,\
                    "use_proportional_connected":False,\
                     "use_proportional_projected":False,\
                      "snap":False, "snap_elements":{'INCREMENT'},\
                       "use_snap_project":False, "snap_target":'CLOSEST',\
                        "use_snap_self":True, "use_snap_edit":True,\
                         "use_snap_nonedit":True, "use_snap_selectable":False,\
                          "snap_point":(0, 0, 0), "snap_align":False,\
                           "snap_normal":(0, 0, 0), "gpencil_strokes":False, \
                           "cursor_transform":False, "texture_space":False,\
                            "remove_on_cancel":False, "use_duplicated_keyframes":False,\
                             "view2d_edge_pan":False, "release_confirm":False,\
                              "use_accurate":False, "use_automerge_and_split":False})
    bpy.ops.object.editmode_toggle()
    #End Edit mode
#end def

#円柱とボーンにウェイトを設定する。オブジェクト名を指定して1組だけ設定
def funcAutomaticWeight(firstObjName,SecondObjName):
    #next 1個ずつ親子設定にしていく、できれば親子関係がすでに設定されていれば何もしないようにしたいが、よくわからない
    gFindOne=""#Flag判定
    gFindTwo=""#Flag判定
    tmpObj=""
    #object mode にしないとオートウェイとが正しく動作しない
    print("now mode is ",bpy.context.mode) #editモードだったら、EDIT_ARMATURE　のように出力される
    if bpy.context.mode == 'OBJECT':
        print("now OBJECT MODE")
    else:
        bpy.ops.object.editmode_toggle()#Objectモードに変更
    #2回ループは非効率的だけど、今はこれでいく　1組のオブジェクトとボーンをウェイト設定
    #Cylinder
    for obj in bpy.data.objects:
        if firstObjName in obj.name:
            print("find obj1")
            tmpObj=obj
            obj.select_set(True)
            gFindOne="ari"
    #Armature
    for obj in bpy.data.objects:
        if SecondObjName in obj.name:
            print("find obj2")
            obj.select_set(True)
            gFindTwo="ari"

    #できれば、すでに親子関係・ウェイトモードが設定されているかを判別したいけど、わからない
    if gFindOne=="ari" and gFindTwo=="ari":
        print("add parent do")
        #bone weight Automatic Weight Ctr+P　オブジェクトモードで実行する必要がある
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    else:
        print("いずれか一方または両方選択できませんでした")

    tmpObj.select_set(False)#Cylinder解除
    bpy.ops.object.editmode_toggle()#Editモードに変更
#end def

def funcSetWiggle2(arm,settingList):#armはアーマチュア名
    #アドオン　wiggle2がインストールされていることが前提
    #settingListOne は、設定のリスト、パラメータ配列、ボーンの数によって設定は個別に異なる
    #head:root,　tail:尻尾揺れる
    bpy.ops.object.mode_set(mode='POSE')

    print("Making Wiggle2")
    if len(settingList) < 1:
        print("配列のパラメータが足りません")
    #2024/10/15　14:36
    #ArmatureからPoseのBone親を探して、子どもに設定する.
    gFindOne=""
    gFindTwo=""
    gWiggleBoneCount=0
    #print("settingList[gWiggleBoneCount] :"+str(settingList[gWiggleBoneCount]))
    boneStrTmp="Bone.000"
    listCount=len(settingList)
    for obj in bpy.data.objects:
        if arm == obj.name:
            #print("find arm")
            obj.select_set(True)
            #gFindOne="ari"
            #Editモードに変更 pose モードにするためだけど効き目がないので無駄なコードかも
            for subbone in obj.pose.bones:
                print("bone::"+subbone.name)
                if "Bone" == subbone.name and gWiggleBoneCount == 0:# Bone in nameにすると含まれるになる
                    print ("bone name:" + str(subbone.name))
                    #次はここから、
                    #☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
                    #2024/10/15　うまくいってない
                    #理由がわかった。ポーズモードでボーンに設定を与えるから、
                    #本来は、ポーズモードで、Amature＞Pose＞Bone、、、Bone007に対して設定を与える。
                    #正しくできなかったのは、Objedtモード状態の　　Amature＞Armature.022＞Bone、、、Bone007に設定してる気がする。
                    #最後に誤りの一番の理由は、Selectしたままにしたので、その値が最後の値で上書きされてしまった。selectを解除が必要だった
                    #2024/10/15
                    #subbone.select_set(True) #ボーンではエラーになるamt.pose.bones['Bone'].bone.select = True
                    subbone.bone.select=True
                    bpy.context.scene.wiggle_enable = True 
                    bpy.context.active_pose_bone.wiggle_head = True #'NoneType' object has no attribute 'wiggle_head'　ポーズモードになっていないとエラー
                    bpy.context.active_pose_bone.wiggle_stiff_head = settingList[gWiggleBoneCount]
                    bpy.context.active_pose_bone.wiggle_tail = False
                    subbone.bone.select=False #解除してなかったので、上書きされた
                    print("パラメータ:"+str(settingList[gWiggleBoneCount]) ) 
                    gWiggleBoneCount=1
                    #他にも設定があるので別の機会に試す
                else:
                    #以下のIF部分は再度構成したほうがよい。たぶん入れ子の構想がまずい気がする。もっとスマートな書き方がある。2024/10/15
                    #ボーンが2桁のときの動作確認はしてない。エラーが出たらごめんね。
                    if gWiggleBoneCount >=1: #少なくとも親ボーン[0]が見つからないと処理しない。子ボーンから001になる
                        boneStrTmpCount=len(boneStrTmp)
                        boneStr=""
                        if gWiggleBoneCount < 10:#1桁の場合
                            #print("ボーン1桁")
                            #boneStrTmpの最後の1文字を数字に置き換える
                            boneStr=boneStrTmp[0:boneStrTmpCount-1]+str(gWiggleBoneCount)
                            #print("ボーン名"+boneStr)
                            
                        elif gWiggleBoneCount >= 10 and gWiggleBoneCount < 100:
                            print("ボーン2桁")
                            #boneStrTmpの最後の2文字を数字に置き換える
                            boneStr=boneStrTmp[0:boneStrTmpCount-2]+str(gWiggleBoneCount)#ここは確認してない
                            
                        elif gWiggleBoneCount >= 100:
                            print("100以上は対応できません。")
                            break

                        if boneStr == subbone.name: 
                            #子ボーン選択 forで対応。もしsettingListの要素数が足りない場合は、最後の値を使用する
                            #2024/10/15
                            #subbone.select_set(True)
                            #bpy.ops.object.mode_set(mode='POSE')
                            subbone.bone.select=True
                            bpy.context.active_pose_bone.wiggle_tail = True
                            #settingListの数が、ボーンの数より小さいときは、最後の値をそのまま使う
                            #2024/10/15
                            if (listCount-1) <  gWiggleBoneCount:
                                bpy.context.active_pose_bone.wiggle_stiff = settingList[-1]#最後の値を挿入
                                print("settingListの数が合っていないので最後の値を使用しました")
                            else:
                                bpy.context.active_pose_bone.wiggle_stiff = settingList[gWiggleBoneCount]
                                print(boneStr+":パラメータ:"+str(settingList[gWiggleBoneCount]) ) 
                                gWiggleBoneCount+=1
                            subbone.bone.select=False #設定したら、選択を解除する
#end def
def funcBoneSimpleAnimation(arm,frame,y):#arm:Armature, frame:timeline frame, y: y distance
    #ArmatureのBoneを少し動かしてアニメーションの自動化補助程度の設定
    #ポーズモードで、ルートボーンを動かすアニメーションの設定までを自動化したい。
    #すでにArmatureが設定されていることが前提で、Armature名、ボーン名などを把握している必要がある
    #keyframe_insert ( data_path、 index = -1、 frame = bpy.context.scene.frame_current、 group = ''、 options = set()、 keytype = 'KEYFRAME' ) 
    #data_path="location"とか"scale"とか"rotation_euler"とかを入れる
    #index ( int ) – キーとなるプロパティの配列インデックス。デフォルトは -1
    #frame ( float ) – キーフレームが挿入されるフレーム。デフォルトは現在のフレームです。なのでbpy.context.scene.frame_set(N)すると不要みたい
    #以降は特に必要なときに調べる
    #
    print("funcBoneSimpleAnimation()")
    localFrame=0
    localFrame=frame
    bpy.ops.object.mode_set(mode='POSE')#モード変更
    for obj in bpy.data.objects:
        if arm == obj.name:
            obj.select_set(True)
            for subbone in obj.pose.bones:
                print("bone::"+subbone.name)
                if "Bone" == subbone.name:# Bone in nameにすると含まれるになる
                    print ("bone name:" + str(subbone.name))
                    subbone.bone.select=True
                    #animation move
                    #Y軸に動かす、フレーム動かす、Y軸から原点に戻す、フレーム動かすの繰り返し
                    #ボーンをlocation.yとするとグローバルではZ軸（上方）に動くので、Z軸に対して動かすとY軸に動く
                    #bpy.context.area.ui_type = 'TIMELINE'
                    #bpy.context.scene.tool_settings.use_keyframe_insert_auto = True
                    bpy.context.scene.frame_set(0)
                    subbone.location.z = 0.0
                    subbone.keyframe_insert(data_path="location")

                    bpy.context.scene.frame_set(localFrame)
                    subbone.location.z = y
                    subbone.keyframe_insert(data_path="location")
                    localFrame+=frame
                    
                    bpy.context.scene.frame_set(localFrame)
                    subbone.location.z = 0 #-y これだと激しいけど、面白いかも
                    subbone.keyframe_insert(data_path="location")
                    localFrame+=frame
                
                    bpy.context.scene.frame_set(localFrame)
                    subbone.location.z = y
                    subbone.keyframe_insert(data_path="location")
                    localFrame+=frame

                    bpy.context.scene.frame_set(localFrame)
                    subbone.location.z = 0
                    subbone.keyframe_insert(data_path="location")

                    #bpy.context.scene.tool_settings.use_keyframe_insert_auto = False
                    bpy.context.scene.frame_end = localFrame+5 #タイムラインのEndを250からキーフレーム＋アルファに短く設定
                    bpy.context.scene.frame_set(0) # フレームを戻しておく
                    subbone.bone.select=False #選択解除
                    return#1個しかないので抜ける
#end def
def funcMatome():
    #ClassCapcelParamaterを使用。クラス化したものをまとめる,クラスにしたことで、オブジェクトが増えてもコード量はそれほど増えない
    #以前は1オブジェクト増加で10行くらいコードが増えたけど、カプセル化で＋1行になった（配列Append分）
    gDepth=6# cylinder hight
    #gCountBones=6#
    testLocation=(0.0,  0.0,    gDepth/2)  #x,y,z

    gClassList=[]#class capcel
    gParamaterList=[]#Wiggle2のパラメータのリスト 200柔らか、＞＞＞　800固い
    #gParamaterList.append({400,500,600,700,800,850})#中括弧これだとうまくいかない　なんでだ？{}で囲ったのが原因だった
    #[]大カッコにした　これで正解
    gParamaterList.append([800,800,800,800,800,800])#配列の要素数は2個以上99未満の個数で記載。要素数は同じ数である必要はない。がわかりやすく同じにしてるだけ
    gParamaterList.append([200,200,200,200,200,200])
    gParamaterList.append([200,300,400,500,600,750])
    gParamaterList.append([800,300,300,300,300,200])
    gParamaterList.append([800,700,600,400,300,200])

    tmpParamaterListCount=len(gParamaterList)
    print("gParamaterList count:"+str(tmpParamaterListCount))

    tmpArmStr="Armature.000"#Armature.001みたいにする
    tmpArmStrCount=len(tmpArmStr)

    tmpCylinderStr="Cylinder.000"
    tmpCylinderStrCount=len(tmpCylinderStr)
    tmpCapcell=""
    tmpKyori=0
    for i in range(tmpParamaterListCount):
        tmpCapcell=""
        if i==0:#0のときは、番号なし
            subArmStr="Armature"
            subCylinderStr="Cylinder"
        else:
            if tmpParamaterListCount < 10:#桁の場合　001－009となる
                subArmStr=      tmpArmStr[0:tmpArmStrCount-1]+str(i)
                subCylinderStr= tmpCylinderStr[0:tmpCylinderStrCount-1]+str(i)
            elif tmpParamaterListCount >=10 and tmpParamaterListCount < 100:
                subArmStr=      tmpArmStr[0:tmpArmStrCount-2]+str(i)
                subCylinderStr= tmpCylinderStr[0:tmpCylinderStrCount-2]+str(i)
            else:
                print("100を超えたので、許容オーバーです。配列の数を99個にしてください")
                return
        print("gParamaterList[i]="+str(gParamaterList[i]))
        tmpCapcell=ClassCapcelParamater(tmpKyori,   subArmStr,  subCylinderStr, gParamaterList[i])
        tmpCapcell.myNamePrint()#自分のクラス名を出力するだけのもの、何に使うかというと単に使用しているクラス名が知りたいだけ、コピペだと誤記が発生するから
        tmpKyori+=1.5#オブジェクトの間隔固定。#円柱Vertices16，半径0.5ｍ、Depth6ｍ　座標：０，０，３ｍ（Depth6ｍ/2）
        gClassList.append(tmpCapcell)#カプセルにしなくてもよいような気がしてるけどまとめたら便利だろう

    #オブジェクトのボーンの数で作業
    for i in range(tmpParamaterListCount):
        testLocation=(float(gClassList[i].kyori), 0.0, gDepth/2)
        #次はここから2024/10/16
        print("len(gClassList[i].list):"+str(len(gClassList[i].list)))
        print("gClassList[i].armName:"+str(gClassList[i].armName))

        funcObjAndBones(testLocation,   gDepth,        len(gClassList[i].list)) #location,high,bonesCountボーンの数,この段階で配列の要素は使用していない
        funcAutomaticWeight(gClassList[i].objName,  gClassList[i].armName)
        funcSetWiggle2(gClassList[i].armName,       gClassList[i].list)#ここで、配列の要素パラメータが必要になる
        funcBoneSimpleAnimation(gClassList[i].armName,  14, 2)#アニメーション設定、移動させるだけ#arm:Armature名, frame:timeline frame, y: y distance
 
    #end for
#end def

#class 各種パラメータ、設定値をカプセル化にして、更に配列にカプセルを挿入させることでコードの視認性をたかめる
#funcMatome()内で使用する
class ClassCapcelParamater:
    def __init__(self,kyori,armName,objName,list) -> None:
        print("class const")
        self.kyori=     kyori#オブジェクトのX座標
        self.armName=   armName#Armature name:Armature
        self.objName=   objName#Obj type name:Cylinder
        self.list=      list#Wiggle2のStiffのパラメータ配列、ボーンの数だけ必要なので、ボーンの数はこの配列の要素数で自動で取得
        self.number=    0

    def __del__(self): 
        print("del デストラクタ、何もしないけど")

    def myNamePrint(self):#  class 自分自身 出力
        function_name = inspect.currentframe().f_code.co_name# この部分は関数中でPrintで使える
        class_name = self.__class__.__name__
        print('{}.{}'.format(function_name, class_name))
#end Class

if __name__ == "__main__":
    print("*************************************************")
    print("*************************************************")
    print("****************** Start  ***********************")
    #main GO
    #gDepth=6# cylinder hight
    #gCountBones=6# bone count over 2 number.limit count is [11 or 12]. << by gDepth:6 
    # 3Dカーソルの位置を元に戻す
    bpy.context.scene.cursor.location=(0.0,0.0,0.0)
    #obj.animation_data_clear()#アニメーションデータクリア
    funcMatome()#Class capcelをまとめたもの

    print("****************** end  ***********************")
    
'''
    #Stiff（固さ）は数値が低いほど柔らかい、数値が高いほど固くなる
    tmp="Armature"#
    #円柱Vertices16，半径0.5ｍ、Depth6ｍ　座標：０，０，３ｍ（Depth6ｍ/2）
    testLocation=(0.0,0.0,gDepth/2)  #x,y,z
    funcObjAndBones(testLocation,gDepth,8) #location,high,bonesCountボーンの数
    funcAutomaticWeight("Cylinder",tmp)
    settingListOne=[400,500,600,700,800,850,900,1000]#ボーンの数分必要になる
    funcSetWiggle2(tmp,settingListOne) #
    funcBoneSimpleAnimation(tmp,14,2)#アニメーション設定、移動させるだけ#arm:Armature名, frame:timeline frame, y: y distance
    bpy.ops.object.mode_set(mode='OBJECT')
'''
    #end main