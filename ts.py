if __name__ == '__main__':
    def getStatus(name, message=None):
    	status = {}
    	if(name == 'SUCESS'):
    		if(message):
    			status['message'] = '<strong>Sucesso! </strong>' + message
    		else:
    			status['message'] = '<strong>Sucesso! </strong> Operação realizada com sucesso.'
    		status['cssClass'] = 'alert-success'
    		return status
    	if(name == 'WARNING'):
    		if(message):
    			status['message'] = '<strong>Aviso! </strong>' + message
    		else:
    			status['message'] = '<strong>Aviso! </strong> A operação não pode ser realizada'
    		status['cssClass'] = 'alert-warning'
    		return status
    	if(name == 'ERROR'):
    		if(message):
    			status['message'] = '<strong>Erro! </strong>' + message
    		else:
    			status['message'] = '<strong>Erro! </strong> Erro ao tentar realizar a operação.'
    		status['cssClass'] = 'alert-danger'
    		return status

    print(getStatus('WARNING'))
