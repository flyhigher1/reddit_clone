# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
# http://hostnames/app/default/index
# http://hostnames/app/default/create_post/<category>
# http://hostnames/app/default/edit_post/<id>
# http://hostnames/app/default/list_posts_by_datetime/<category>/<page>
# http://hostnames/app/default/list_post_by_votes/<category>/<page>
# http://hostnames/app/default/list_post_by_author/<userid>/<page>
# http://hostnames/app/default/view_post/<id>
# http://hostnames/app/default/vote_post/<id>/<up or down>
# http://hostnames/app/default/comm_vote_post/<comment id>/up or down>

# ---- example index page ----
POST_PER_PAGE = 10

def get_category():
    category_name = request.args(0)
    category = db.category(name=category_name )
    if not category:
        session.flash = "page not found 404"
        redirect(URL('index'))
    return category

def index():
    rows = db(db.category).select()
    return locals()

def create_post():
    category = get_category()
    db.post.category.default = category.id
    form = SQLFORM(db.post).process(next='view_posts/[id]')

    return locals()

def edit_post():
    id = request.args(0, cast=int, default=0)
    form = SQLFORM(db.post, id).process(next='view_posts/[id]')
    return locals()

def list_posts_by_datetime():
    category = get_category()
    page = request.args(1, cast=int, default=0)
    start = page*POST_PER_PAGE
    stop = start+POST_PER_PAGE
    rows = db(db.post.category == category.id).select(orderby=~db.post.created_on, limitby=(start, stop))
    return locals()

def list_posts_by_votes():
    category = get_category()
    page = request.args(1, cast=int, default=0)
    start = page*POST_PER_PAGE
    stop = start+POST_PER_PAGE
    rows = db(db.post.category == category.id).select(orderby=~db.post.votes, limitby=(start, stop))
    return locals()

def list_posts_by_author():
    user_id = request.args(0, cast=int)
    page = request.args(1, cast=int, default=0)
    start = page*POST_PER_PAGE
    stop = start+POST_PER_PAGE
    rows = db(db.post.created_by == user_id).select(orderby=~db.post.created_on, limitby=(start, stop))
    return locals()

def view_posts():
    id = request.args(0, cast=int)
    post = db.post(id) or redirect(URL('index'))
    comments = db(db.comm.post == post.id).select(orderby=~db.comm.created_on)
    ## TODO
    return locals()

def vote_callback():
    id = request.args(0, cast=int)
    direction = request.args(1)
    ## TODO
    return locals()

def comm_vote_callback():
    id = request.args(0, cast=int)
    ## TODO
    return locals()

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
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

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
