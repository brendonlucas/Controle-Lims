# Controle-Lims
<h1>Dados importantes que precisam estar registrados no banco de dados para funcionar corretamente!</h1>
<li><h2>Tipos de Emprestimos </h2></li>
<pre><code>
from emprestimo.models import *
TipoEstadoEmprestimo(nome='Emprestado', descricao='O Emprestimo foi realizado').save()
TipoEstadoEmprestimo(nome='Devolvido', descricao='O Emprestimo foi finalizado').save()</code></pre>
    
OBS: Devem ser criados nesta mesma ordem, para evitar falhas.


<li><h2>Tipos de Usuario </h2></li>
<pre><code>
from controle.models import *
TipoUsuario(nome='Normal', descricao='Usuario com acesso limitado').save()
TipoUsuario(nome='Administrador', descricao='Usuario com acesso total ao sistema').save()</code></pre>
    
OBS: Devem ser criados nesta mesma ordem, para evitar falhas.

<li><h2>Tipos de Equipamento </h2></li>
<pre><code>
from controle.models import *
TipoEquipamento(nome='Consumivel', descricao='Item do tipo consumivel que pode sofrer perda').save()
TipoEquipamento(nome='Permanente', descricao='Item do tipo Permanente que caso haja perda, medidas serão tomadas').save()</code></pre>
    
OBS: Devem ser criados nesta mesma ordem, para evitar falhas.
