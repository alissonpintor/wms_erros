% rebase('base.html', title='Produtos Cadastrados')
<div id='main' class="row">
    <div class="col-md-12">
        <div class="page-header">
            <h1>Pagina Administrativa</h1>
        </div>
        <p>Bem Vindo {{current_user.username}}, your role is: {{current_user.role}}, access time: {{current_user.session_accessed_time}}</p>
    </div>
    <div class="col-md-6">
        <h2>Create new user:</h2>
        <form action="create_user" method="post">
            <div class="form-group">
                <label for="username">Usuário</label>
                <input type="text" class="form-control" name="username" id="username">
            </div>
            <div class="form-group">
                <label for="role">Acesso</label>
                <input type="text" class="form-control" name="role" id="role">
            </div>
            <div class="form-group">
                <label for="password">Senha</label>
                <input type="password" class="form-control" name="password" id="password">
            </div>
            <button type="submit" class="btn btn-default"> OK </button>
        </form>

        <h2>Delete user:</h2>
        <form action="delete_user" method="post">
            <div class="form-group">
                <label for="username">Usuário</label>
                <input type="text" class="form-control" name="username" id="username">
            </div>
            <button type="submit" class="btn btn-default"> OK </button>
        </form>

        <h2>Create new role:</h2>
        <form action="create_role" method="post">
            <div class="form-group">
                <label for="role">Acesso</label>
                <input type="text" class="form-control" name="role" id="role">
            </div>
            <div class="form-group">
                <label for="level">Level</label>
                <input type="text" class="form-control" name="level" id="level">
            </div>
            <button type="submit" class="btn btn-default"> OK </button>
        </form>

        <h2>Delete role:</h2>
        <form action="delete_role" method="post">
            <div class="form-group">
                <label for="role">Acesso</label>
                <input type="text" class="form-control" name="role" id="role">
            </div>
            <button type="submit" class="btn btn-default"> OK </button>
        </form>
    </div>

    <div class="col-md-6" id="users">
        <table class="table">
            <tr>
                <th>Username</th>
                <th>Role</th>
                <th>Email</th>
                <th>Description</th>
            </tr>
            %for u in users:
            <tr>
                <td>{{u[0]}}</td>
                <td>{{u[1]}}</td>
                <td>{{u[2]}}</td>
                <td>{{u[2]}}</td>
            </tr>
            %end
        </table>
        <br/>
        <table class="table">
            <tr>
                <th>Role</th>
                <th>Level</th>
            </tr>
            %for r in roles:
            <tr>
                <td>{{r[0]}}</td>
                <td>{{r[1]}}</td>
            </tr>
            %end
        </table>
        <p>(Reload page to refresh)</p>
    </div>

    <div class="clear"></div>

    <div id='status'>
        <p>Ready.</p>
    </div>
    <script>
        // Prevent form submission, send POST asynchronously and parse returned JSON
        $('form').submit(function() {
            $("div#status").fadeIn(100);
            z = $(this);
            $.post($(this).attr('action'), $(this).serialize(), function(j) {
                if (j.ok) {
                    $("div#status").css("background-color", "#f0fff0");
                    $("div#status p").text('Ok.');
                } else {
                    $("div#status").css("background-color", "#fff0f0");
                    $("div#status p").text(j.msg);
                }
                $("div#status").delay(800).fadeOut(500);
            }, "json");
            return false;
        });
    </script>
</div>
<!--
<style>
div#commands { width: 45%%; float: left}
div#users { width: 45%; float: right}
div#main {
    color: #777;
    margin: auto;
    margin-left: 5em;
    font-size: 80%;
}
input {
    background: #f8f8f8;
    border: 1px solid #777;
    margin: auto;
}
input:hover { background: #fefefe}
label {
  width: 8em;
  float: left;
  text-align: right;
  margin-right: 0.5em;
  display: block
}
button {
    margin-left: 13em;
}
button.close {
    margin-left: .1em;
}
div#status {
    border: 1px solid #999;
    padding: .5em;
    margin: 2em;
    width: 15em;
    -moz-border-radius: 10px;
    border-radius: 10px;
}
.clear { clear: both;}
div#urls {
  position:absolute;
  top:0;
  right:1em;
}
</style>
-->
