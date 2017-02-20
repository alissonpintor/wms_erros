<!DOCTYPE html>
<html>

<head>
    <title>Login</title>

    <meta charset="utf-8" / />

    <link rel="stylesheet" type="text/css" href="/normalize.css">
    <link rel="stylesheet" type="text/css" href="/bootstrap.min.css">
    <!--<link rel="stylesheet" type="text/css" href="dataTables.bootstrap.min.css">-->
    <link rel="stylesheet" type="text/css" href="/bootstrap-table.min.css">
    <link rel="stylesheet" type="text/css" href="/jquery-ui.min.css">
    <link rel="stylesheet" type="text/css" href="/style.css">
    <link rel="icon" href="/icone.png">
</head>

<body>
    <div class="container">
        <div class="row">
            <div class="col-md-4 col-md-offset-4">
                <div class="page-header">
                  <h1>Login</h1>
                </div>
                <form action="login" method="post" name="login">
                    <div class="form-group">
                        <label for="username">Usuário</label>
                        <input type="text" class="form-control" name="username" id="username">
                    </div>
                    <div class="form-group">
                        <label for="password">Senha</label>
                        <input type="password" class="form-control" name="password" id="username">
                    </div>
                    <button type="submit" class="btn btn-default"> OK </button>
                </form>
                <br />
            </div>
        </div>
    </div>
    <script src="/jquery.js" type="text/javascript" charset="utf-8"></script>
    <script src="/jquery-ui.min.js" type="text/javascript" charset="utf-8"></script>
    <script src="/bootstrap.min.js" type="text/javascript" charset="utf-8"></script>
</body>

</html>
