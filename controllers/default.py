# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################


@auth.requires_login()
def index():
    db.case_file.id.readable=False
    db.case_file_history.id.readable=False
    db.case_file_history.case_file_id.readable=False
    db.case_file_child.case_file_id.readable=False
    db.case_file_child.id.readable=False
    if auth.has_membership("admin"):
        if 'case_file_history.case_file_id' in request.args:
            form = SQLFORM.smartgrid(db.case_file, orderby=~db.case_file_history.id)
        else:
            form = SQLFORM.smartgrid(db.case_file, orderby=~db.case_file.id, oncreate=add_movement)
        return dict(form=form)
    elif auth.has_membership("read_only"):
        if 'case_file_history.case_file_id' in request.args:
            form = SQLFORM.smartgrid(db.case_file, orderby=~db.case_file_history.id)
        else:
            form = SQLFORM.smartgrid(db.case_file, orderby=~db.case_file.id, oncreate=add_movement,
                    field_id=False,
                    create=False,
                    deletable=False,
                    editable=False,
                    csv=False)
        return dict(form=form)
    elif auth.has_membership("write_only"):
        if 'case_file_history.case_file_id' in request.args:
            form = SQLFORM.smartgrid(db.case_file, orderby=~db.case_file_history.id)
        else:
            form = SQLFORM.smartgrid(db.case_file, orderby=~db.case_file.id, oncreate=add_movement,
                    field_id=False,
                    create=True,
                    editable=True,
                    deletable=False,
                    csv=False)
        return dict(form=form)
    else:
        return dict(form='')

def add_movement(form):
    return redirect(URL('index', args=['case_file','case_file_history.case_file_id',form.vars.id,'new','case_file_history'], user_signature=True))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


