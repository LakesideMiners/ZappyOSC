GPL

Requires 
Poi Toon
https://github.com/poiyomi/PoiyomiToonShader

VRLab's Avatar 3.0 Manager
https://github.com/VRLabs/Avatars-3.0-Manager

ZappyOSC
https://github.com/LakesideMiners/ZappyOSC



1. Drag the PiShock prefab into the unity scene, then move it into your avatar hierarchy. it should look like this afterwards

Your Avatar
|
|_ _ Body
|
|_ _ Armature
|
|_ _ PiShock

2. Move, scale, and rotate the PiShock to where you want it on your avatar.

3. Locate the Parent Constraint componet, and then add in the bone that you want to constrain it to, then hit ONLY activate.

4. Use the VRLab's Avatar 3.0 Manager to merge PiSHockFX to your avatar's FX layer and the PiShockPrams to your avatar's Paramaters.


5. add the submenu "PiShockMenu" to your avatar's menu.


6. Make sure to set the "Anchor Override" on the "Mesh Renderer" Component to something like your Hip bone to avoid lighting issues.