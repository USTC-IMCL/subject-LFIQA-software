<<<<<<< HEAD
import cv2
import numpy as np

_INTERP_METHOD_MAP = {
    "nearest": cv2.INTER_NEAREST,	
    "linear" : cv2.INTER_LINEAR,
    "cubic"  : cv2.INTER_CUBIC
}

def _check_parameter_and_return(input_data, param_name):
    assert param_name in input_data and isinstance(input_data[param_name], (int, float)), f"Missing input parameter {param_name}, and its type only support int and float"
    return input_data[param_name]

def lf_shift_sum(lf_image : np.ndarray, 
                 slope : float, 
                 filt_options : dict):
    """
        This filter works by shifting all u,v slices of the light field to a common depth, then adding the slices together to yield a single 2D output.  
        The effect is very similar to planar focus, and by controlling the amount of shift one may focus on different depths.  
        If a weight channel is present in the light field it gets used during normalization.

        Inputs:
            LF : The light field to be filtered 
            Slope : The amount by which light field slices should be shifted, this encodes the depth at which the output will
                    be focused. The relationship between slope and depth depends on light field parameterization, but in
                    general a slope of 0 lies near the center of the captured depth of field.
            [optional] FiltOptions : struct controlling filter operation
                 Precision : 'single' or 'double', default 'single'
                  Aspect4D : aspect ratio of the light field, default [1 1 1 1]
                 Normalize : default true; when enabled the output is normalized so that darkening near image edges is removed
             FlattenMethod : 'Sum' or 'Max', default 'Sum'; when the shifted light field slices are combined,
                             they are by default added together, but max can also yield useful results.
              InterpMethod : default 'linear'; this is passed on to interpn to determine how shifted light field slices
                             are found; other useful settings are 'nearest', 'cubic' and 'spline'
                 ExtrapVal : default 0; when shifting light field slices, pixels falling outside the input light field
                             are set to this value
                 MinWeight : during normalization, pixels for which the output value is not well defined (i.e. for
                             which the filtered weight is very low) get set to 0. MinWeight sets the threshold at which
                             this occurs, default is 10 * the numerical precision of the output, as returned by eps

        Outputs:
            img_out : A 2D filtered image
    """
    Normalize     = filt_options.get('Normalize', True)
    MinWeight     = filt_options.get('MinWeight', 10 * 2 ** -23)
    Aspect4D      = filt_options.get('Aspect4D', [1])
    FlattenMethod = filt_options.get('FlattenMethod', 'sum').lower()
    InterpMethod  = filt_options.get('InterpMethod', 'linear')
    ExtrapVal     = filt_options.get('ExtrapVal', 0)

    assert InterpMethod in _INTERP_METHOD_MAP, f"support three interp method ['nearest', 'linear', 'cubic'], but input {InterpMethod}"
    InterpMethod = _INTERP_METHOD_MAP[InterpMethod]


    if len(Aspect4D) == 1:
        Aspect4D = Aspect4D[0] * np.array([1.0, 1.0, 1.0, 1.0])

    lf_size     = lf_image.shape
    ncol_chans  = lf_image.shape[4]     
    has_weight  = (ncol_chans == 4 or ncol_chans == 2)
    if has_weight:
        ncol_chans = ncol_chans - 1

    lf_image = lf_image.astype('float')

    if Normalize:
        if has_weight:
            for icol_chann in range(ncol_chans):
                lf_image[..., icol_chann] = lf_image[..., icol_chann] * lf_image[..., -1]
        else:   #   add a weight cahnnel
            trans_lf_image  = lf_image.transpose(4,0,1,2,3)
            weight_chan     = np.expand_dims(np.ones(trans_lf_image[0, ...].shape), axis=0)
            trans_lf_image  = np.vstack([trans_lf_image, weight_chan])
            lf_image        = trans_lf_image.transpose(1,2,3,4,0)

    tv_slope = slope * Aspect4D[2] / Aspect4D[0]
    su_slope = slope * Aspect4D[3] / Aspect4D[1]

    vv_2d, uu_2d = np.meshgrid([x for x in range(lf_size[2])],
                               [y for y in range(lf_size[3])])
    vv_2d = vv_2d.astype(np.float32)
    uu_2d = uu_2d.astype(np.float32)
    vvec = np.linspace(-0.5, 0.5, lf_size[0]) * tv_slope * lf_size[0]
    uvec = np.linspace(-0.5, 0.5, lf_size[1]) * su_slope * lf_size[1]

    for t_idx in range(lf_size[0]):
        v_offset = vvec[t_idx]
        for s_idx in range(lf_size[1]):
            u_offset = uvec[s_idx]

            for i_chan in range(lf_size[-1]):
                cur_slice  = np.squeeze(lf_image[t_idx, s_idx, :, :, i_chan])
                
                interp_slice = cv2.remap(cur_slice.T, vv_2d + v_offset, uu_2d + u_offset, interpolation=cv2.INTER_CUBIC)
                interp_slice[np.isnan(interp_slice)] = ExtrapVal

                lf_image[t_idx, s_idx, :, :, i_chan] = interp_slice.T

    if FlattenMethod == 'sum':
        img_out = np.squeeze(np.sum(lf_image, axis=(0, 1)))
    elif FlattenMethod == 'max':
        img_out = np.reshape(lf_image, (lf_size[0] * lf_size[1], -1))
        img_out = np.max(img_out, axis=0)
        img_out = np.reshape(img_out, tuple(lf_size[2:]))
    else:
        raise ValueError(f"FlattenMethod only support ['sum', 'max'], but get {FlattenMethod}")
    
    if Normalize:
        weight_chan = img_out[..., -1]
        for icol_chan in range(ncol_chans):
            img_out[:,:,icol_chan] = img_out[:,:,icol_chan] / (weight_chan + MinWeight)
    return img_out 


def compute_slope(device_meta : dict, 
                  depth_lambda : dict,
                  depth_value : int):
    maxLambda = _check_parameter_and_return(depth_lambda, 'LambdaMax')
    minLambda = _check_parameter_and_return(depth_lambda, 'LambdaMin')

    focal_length    = _check_parameter_and_return(device_meta, 'focalLength') * 10**5 
    f_number        = _check_parameter_and_return(device_meta, 'fNumber')
    infinity_lambda = _check_parameter_and_return(device_meta, 'infinityLambda')
    lens_pitch      = _check_parameter_and_return(device_meta, 'lens_pitch') * 10**5

    distance = focal_length + infinity_lambda * f_number * lens_pitch
    aperture = focal_length / f_number

    current_lambda      = depth_value / 255 * (maxLambda - minLambda) + minLambda
    current_distance    = current_lambda * f_number * lens_pitch
    slope               = current_distance/ (distance - current_distance) * (aperture / 15) / lens_pitch
    # refcous_img         = lf_shift_sum(lf_image, slope, {"InterpMethod":'cubic'})

    return slope


def run_refocus(lf_image : np.ndarray,
                device_meta : dict,
                depth_lambda : dict,
                depth_value : int,
                filt_options : dict
                ):
    slope       = compute_slope(device_meta, depth_lambda, depth_value)
    refcous_img = lf_shift_sum(lf_image, slope, filt_options)
    return refcous_img

=======
import cv2
import numpy as np

_INTERP_METHOD_MAP = {
    "nearest": cv2.INTER_NEAREST,	
    "linear" : cv2.INTER_LINEAR,
    "cubic"  : cv2.INTER_CUBIC
}

def _check_parameter_and_return(input_data, param_name):
    assert param_name in input_data and isinstance(input_data[param_name], (int, float)), f"Missing input parameter {param_name}, and its type only support int and float"
    return input_data[param_name]

def lf_shift_sum(lf_image : np.ndarray, 
                 slope : float, 
                 filt_options : dict):
    """
        This filter works by shifting all u,v slices of the light field to a common depth, then adding the slices together to yield a single 2D output.  
        The effect is very similar to planar focus, and by controlling the amount of shift one may focus on different depths.  
        If a weight channel is present in the light field it gets used during normalization.

        Inputs:
            LF : The light field to be filtered 
            Slope : The amount by which light field slices should be shifted, this encodes the depth at which the output will
                    be focused. The relationship between slope and depth depends on light field parameterization, but in
                    general a slope of 0 lies near the center of the captured depth of field.
            [optional] FiltOptions : struct controlling filter operation
                 Precision : 'single' or 'double', default 'single'
                  Aspect4D : aspect ratio of the light field, default [1 1 1 1]
                 Normalize : default true; when enabled the output is normalized so that darkening near image edges is removed
             FlattenMethod : 'Sum' or 'Max', default 'Sum'; when the shifted light field slices are combined,
                             they are by default added together, but max can also yield useful results.
              InterpMethod : default 'linear'; this is passed on to interpn to determine how shifted light field slices
                             are found; other useful settings are 'nearest', 'cubic' and 'spline'
                 ExtrapVal : default 0; when shifting light field slices, pixels falling outside the input light field
                             are set to this value
                 MinWeight : during normalization, pixels for which the output value is not well defined (i.e. for
                             which the filtered weight is very low) get set to 0. MinWeight sets the threshold at which
                             this occurs, default is 10 * the numerical precision of the output, as returned by eps

        Outputs:
            img_out : A 2D filtered image
    """
    Normalize     = filt_options.get('Normalize', True)
    MinWeight     = filt_options.get('MinWeight', 10 * 2 ** -23)
    Aspect4D      = filt_options.get('Aspect4D', [1])
    FlattenMethod = filt_options.get('FlattenMethod', 'sum').lower()
    InterpMethod  = filt_options.get('InterpMethod', 'linear')
    ExtrapVal     = filt_options.get('ExtrapVal', 0)

    assert InterpMethod in _INTERP_METHOD_MAP, f"support three interp method ['nearest', 'linear', 'cubic'], but input {InterpMethod}"
    InterpMethod = _INTERP_METHOD_MAP[InterpMethod]


    if len(Aspect4D) == 1:
        Aspect4D = Aspect4D[0] * np.array([1.0, 1.0, 1.0, 1.0])

    lf_size     = lf_image.shape
    ncol_chans  = lf_image.shape[4]     
    has_weight  = (ncol_chans == 4 or ncol_chans == 2)
    if has_weight:
        ncol_chans = ncol_chans - 1

    lf_image = lf_image.astype('float')

    if Normalize:
        if has_weight:
            for icol_chann in range(ncol_chans):
                lf_image[..., icol_chann] = lf_image[..., icol_chann] * lf_image[..., -1]
        else:   #   add a weight cahnnel
            trans_lf_image  = lf_image.transpose(4,0,1,2,3)
            weight_chan     = np.expand_dims(np.ones(trans_lf_image[0, ...].shape), axis=0)
            trans_lf_image  = np.vstack([trans_lf_image, weight_chan])
            lf_image        = trans_lf_image.transpose(1,2,3,4,0)

    tv_slope = slope * Aspect4D[2] / Aspect4D[0]
    su_slope = slope * Aspect4D[3] / Aspect4D[1]

    vv_2d, uu_2d = np.meshgrid([x for x in range(lf_size[2])],
                               [y for y in range(lf_size[3])])
    vv_2d = vv_2d.astype(np.float32)
    uu_2d = uu_2d.astype(np.float32)
    vvec = np.linspace(-0.5, 0.5, lf_size[0]) * tv_slope * lf_size[0]
    uvec = np.linspace(-0.5, 0.5, lf_size[1]) * su_slope * lf_size[1]

    vvec = vvec.astype(np.float32)
    uvec = uvec.astype(np.float32)

    for t_idx in range(lf_size[0]):
        v_offset = vvec[t_idx]
        for s_idx in range(lf_size[1]):
            u_offset = uvec[s_idx]

            for i_chan in range(lf_size[-1]):
                cur_slice  = np.squeeze(lf_image[t_idx, s_idx, :, :, i_chan])
                
                interp_slice = cv2.remap(cur_slice.T, vv_2d + v_offset, uu_2d + u_offset, interpolation=cv2.INTER_CUBIC)
                interp_slice[np.isnan(interp_slice)] = ExtrapVal

                lf_image[t_idx, s_idx, :, :, i_chan] = interp_slice.T

    if FlattenMethod == 'sum':
        img_out = np.squeeze(np.sum(lf_image, axis=(0, 1)))
    elif FlattenMethod == 'max':
        img_out = np.reshape(lf_image, (lf_size[0] * lf_size[1], -1))
        img_out = np.max(img_out, axis=0)
        img_out = np.reshape(img_out, tuple(lf_size[2:]))
    else:
        raise ValueError(f"FlattenMethod only support ['sum', 'max'], but get {FlattenMethod}")
    
    if Normalize:
        weight_chan = img_out[..., -1]
        for icol_chan in range(ncol_chans):
            img_out[:,:,icol_chan] = img_out[:,:,icol_chan] / (weight_chan + MinWeight)
    return img_out 


def compute_slope(device_meta : dict, 
                  depth_lambda : dict,
                  depth_value : int):
    maxLambda = _check_parameter_and_return(depth_lambda, 'LambdaMax')
    minLambda = _check_parameter_and_return(depth_lambda, 'LambdaMin')

    focal_length    = _check_parameter_and_return(device_meta, 'focalLength') * 10**5 
    f_number        = _check_parameter_and_return(device_meta, 'fNumber')
    infinity_lambda = _check_parameter_and_return(device_meta, 'infinityLambda')
    lens_pitch      = _check_parameter_and_return(device_meta, 'lens_pitch') * 10**5

    distance = focal_length + infinity_lambda * f_number * lens_pitch
    aperture = focal_length / f_number

    current_lambda      = depth_value / 255 * (maxLambda - minLambda) + minLambda
    current_distance    = current_lambda * f_number * lens_pitch
    slope               = current_distance/ (distance - current_distance) * (aperture / 15) / lens_pitch
    # refcous_img         = lf_shift_sum(lf_image, slope, {"InterpMethod":'cubic'})

    return slope


def run_refocus(lf_image : np.ndarray,
                device_meta : dict,
                depth_lambda : dict,
                depth_value : int,
                filt_options : dict
                ):
    slope       = compute_slope(device_meta, depth_lambda, depth_value)
    refcous_img = lf_shift_sum(lf_image, slope, filt_options)
    return refcous_img

>>>>>>> 4d2b53ec5643d16446214c84b74235e41065f8d7
