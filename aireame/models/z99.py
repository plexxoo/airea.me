if request.env.http_user_agent:
    import os
    detect = local_import("detect")
        
    
    is_mobile = detect.detect_mobile_browser(request.env.http_user_agent)
    #forzar vista movil:
    #is_mobile = True
    if is_mobile:
        #Es un movil             
        response.view = "%s/%s.%s" % (request.controller, request.function, "mobile")
        if not os.path.exists(os.path.join(request.folder, 'views', request.controller, request.function+".mobile")):
            response.view = '%s.%s' % ("generic", "mobile") 
