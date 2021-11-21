def approve_reject(req , action):

    if   action == 'approve'  or action==  'Approve':
        req.is_approved = True
        req.is_closed = True
        req.save()
        status = 'Approved'
    else :
        req.is_cancelled = True
        req.is_closed = True
        req.save()
        status = 'Rejected'
    return status