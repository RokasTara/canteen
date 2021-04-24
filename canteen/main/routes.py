from flask import render_template, request, Blueprint
from canteen.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template("home.html", posts=posts)

@main.route('/about')
def about():
    return render_template("about.html")

    return render_template("create_form.html", title="New Form", form=form)