$(function() {
    $("#messages").delay(3000).toggle(700);

    /* ########################################################################
      EVENTOS JAVASCRIPT DA PAGINA DE CADASTRO DE TIPOS DE TAREFAS
    ######################################################################## */

    //Evento para criar os botoes alterar e novo ao alterar um registro
    $('.update_tarefa').click(function(e) {
        e.preventDefault();
        var id = $(this).closest('tr').find('td:eq(1)').html();
        var descricao = $(this).closest('tr').find('td:eq(2)').html();
        $("#id_tarefa").val(id);
        $("#descricao_tarefa").val(descricao);
        $("#form-button").html("Alterar");
        $("#tarefas-form").attr('action', '/exibir_tarefas/alterar');

        var $novo = $(document.createElement('button'));
        $novo.addClass('btn btn-primary');
        $novo.attr('id', 'form-button-02');
        $novo.html('Novo');
        $novo.on('click', function(e){
            e.preventDefault();
            $("#id_tarefa").val('id');
            $("#descricao_tarefa").val('');
            $("#form-button").html("Cadastrar");
            $novo.remove();
        });
        $("#erros-form").append($novo);
    });

    /* ########################################################################
      EVENTOS JAVASCRIPT DA PAGINA DE CADASTRO DE TIPOS DE ERROS
    ######################################################################## */

    //Evento para criar os botoes alterar e novo ao alterar um registro
    $('.update').click(function(e) {
        e.preventDefault();
        var id = $(this).closest('tr').find('td:eq(1)').html();
        var descricao = $(this).closest('tr').find('td:eq(2)').html();
        var separacao = $(this).closest('tr').find('td:eq(3)').html();

        $("#id_erro").val(id);
        $("#descricao_erro").val(descricao);
        $("option").each(function(i, v){
          if($(v).html() == separacao){
            $(v).attr('selected', 'selected');
          };
        });
        $("#form-button").html("Alterar");
        $("#erros-form").attr('action', '/exibir_erros/alterar');

        var $novo = $(document.createElement('button'));
        $novo.addClass('btn btn-primary');
        $novo.attr('id', 'form-button-02');
        $novo.html('Novo');
        $novo.on('click', function(e){
            e.preventDefault();
            $("#id_erro").val('id');
            $("#descricao_erro").val('');
            $("#tipo_tarefa").val('');
            $("#form-button").html("Cadastrar");
            $novo.remove();
        });
        $("#erros-form").append($novo);
    });

    /* ########################################################################
      EVENTOS JAVASCRIPT DA PAGINA DE CADASTRO DE ERROS DOS COLABORADORES
    ######################################################################## */

    //Chama o Ajax para buscar o cliente da onda digitada
    $('#id_onda').on('blur', function(){
        busca_dados($('#id_onda'), $('#id_produto'), $('#nome_cliente'), $('#form-onda'), '/buscar_pedido')
      }
    );

    //Chama o Ajax para buscar a descrição do produto digitado
    $('#id_produto').on('blur', function(){
        busca_dados($('#id_produto'), $('#id_onda'), $('#descricao_produto'), $('#form-produto'), '/buscar_produto')
      }
    );

    //Função Ajax para buscar os dados de cliente da onda e produto
    function busca_dados(id_input, id_input_02, id_descricao, div, source) {
        $(div).removeClass('has-error');
        $(div).find('span').remove();
        $(id_descricao).val('');
        $('#colaborador').val('');

        if ($(id_input).val() != '') {
            var txt = $(id_input).serialize();
            var id = $(id_input).val();
            $(id_input).attr('readonly', 'readonly');
            $(id_input).val('Carregando...');

            $.ajax({
                type: "GET",
                url: source,
                dataType: "json",
                data: txt,
                success: function(data) {
                    $(id_descricao).val(data);
                    $(id_input).val(id);
                    $(id_input).removeAttr('readonly');
                },
                error: function() {
                    $(id_descricao).val('');
                    $(id_input).val(id);
                    $(id_input).removeAttr('readonly');
                    $(div).addClass('has-error');
                    $(div).append(
                        '<span id="helpBlock2" class="help-block">' +
                        'O valor informado nao foi encontrado.' +
                        '</span>'
                    )
                }
            });

            if($(id_input_02).val() != ''){
              var txt2 = $(id_input_02).serialize();
              var data = txt+'&'+txt2

              $.ajax({
                  type: "GET",
                  url: "/buscar_colaborador",
                  dataType: "json",
                  data: data,
                  success: function(data) {
                      $('#colaborador').val(data);
                  },
                  error: function() {
                      $('#colaborador').val('');
                  }
              });
            }
        }
    }

    //Evento para buscar tarefas
    $('#tipo_tarefa').on('change', function(){
      var id_tarefa = $('#tipo_tarefa option:selected').attr('value');
      console.log(id_tarefa);
      if(id_tarefa){
        $.ajax({
            type: "GET",
            url: "/buscar_erros/"+id_tarefa,
            dataType: "json",
            success: function(data) {
                $('#tipo_erro').html('');
                console.log(data);
                if(data.length > 0){
                  $(data).each(function(key, value){
                    $('#tipo_erro').append(
                      '<option value="'+value.id+'">'+value.descricao+'</option>'
                    );
                    $('#tipo_erro').removeAttr('disabled');
                  });
                }
            },
            error: function() {
                $('#colaborador').val('');
            }
        });
      }else{
        $('#tipo_erro').html('');
        $('#tipo_erro').attr('disabled', 'disabled');
      }
    });
});