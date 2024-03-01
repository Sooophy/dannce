function transferParams(path_to_cam_params, path_to_video, output_path, n_landmarks)
%transferParams Transfers stroke rig calibration parameters into a
%label3d_dannce.mat file.
%   path_to_cam_params (string): path to camera_parameters.mat file
%   path_to_video (string): path to a video file, from which we will
%       extract the total number of frames
%   output_path (string): path denoting the file into which everything will
%       be saved as output
%   n_landmarks (int): number of landmarks to be tracked
%
% Example: transferParams('C:\Users\segura-behavior\camera_calibration\10262021_AprilTag\camera_params.mat','C:\Users\segura-behavior\camera_calibration\10262021_cylinder_Mouse_1\videos\Camera1\0.mp4','C:\Users\segura-behavior\camera_calibration\10262021_cylinder_Mouse_1\label3d_dannce.mat',22)
% transferParams('D:\1files\1Duke\Lab\behavior\stroke_pipeline_codes\12022021_AprilTags\camera_params.mat','','D:\1files\1Duke\Lab\behavior\stroke_pipeline_codes\12022021_AprilTags\label3d_dannce.mat',22)

c = load(path_to_cam_params);
% v = VideoReader(path_to_video);
% total_frames = v.NumFrames;
total_frames = 30000;

camnames = {'Camera1','Camera2','Camera3','Camera4','Camera5','Camera6'};

for i = 1:6
    params{i} = struct();
    params{i}.K = c.params_individual{i}.IntrinsicMatrix;
    params{i}.RDistort = c.params_individual{i}.Intrinsics.RadialDistortion;
    params{i}.TDistort = c.params_individual{i}.Intrinsics.TangentialDistortion;
    params{i}.r = c.rotationMatrix{i};
    params{i}.t = c.translationVector{i};
    
    sync{i} = struct();
    sync{i}.data_2d = zeros(total_frames,2*n_landmarks);
    sync{i}.data_3d = zeros(total_frames,3*n_landmarks);
    sync{i}.data_frame = 1:total_frames;
    sync{i}.data_sampleID = 1:total_frames;
end

params= params'
sync= sync';
display(['Saving to ' output_path]); 
save(output_path,'camnames','params','sync');



end
