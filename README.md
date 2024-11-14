** Simulação de execução fora de ordem com scoreboarding **

Programa a ser executado, em assembly do RISC-V, contendo apenas instruções de um determinado subconjunto. Um exemplo de programa é:
fld f1, 0(x1)
fld f5, 0(x1)
fdiv f2, f4, f5

Configuração das Unidades Funcionais, indicando a quantidade de unidades de cada tipo, e o número de ciclos necessários para completar a execução naquela unidade. Um exemplo de configuração é:
int 2 1
mult 2 4
add 1 2
div 1 10
Este exemplo indica que há duas unidades de processamento de operações inteiras (int) que levam 1 ciclo de execução, duas unidades para multiplicação em ponto flutuante (mult) que levam 4 ciclos, uma unidade de soma em ponto flutuante que leva 2 ciclos, e uma unidade de divisão em ponto flutuante que leva 10 ciclos para completar sua execução.

A saída do simulador é uma tabela indicando o número do ciclo em que cada instrução cada uma das etapas de sua execução com scoreboard: Issue, Read (Leitura de Operandos), Execute (completar execução), Write (escrita de resultados no banco de registradores).

Instruction/Cicle	Issue	Read	Execute	Write
fld f1, 0(x1)	1	2	3	4
fld f5, 0(x1)	2	3	4	5
fdiv f2, f4, f5	3	6	16	17



Não há implementação funcional das instruções; apenas são identificadas as dependências e fluxo de dados para obter a simulação de ciclos de execução.

Entradas e testes
Para a seguinte configuração:

int 1 1
mult 2 4
add 1 2
div 1 10

e o seguinte código de entrada:

fld  f1, 100(x7)
fmul f2, f2, f4
fadd f2, f1, f3
fld  f9, 0(x3)
fdiv f3, f1, f7
fsub f6, f3, f4
fmul f7, f1, f2
fadd f4, f5, f2
fsd  f1, 50(x11)

o resultado  é:

Instruction/Cicle	Issue	Read	Execute	Write
fld f1, 100(x7)	1	2	3	4
fmul f2, f2, f4	2	3	7	8
fadd f2, f1, f3	9	10	12	13
fld f9, 0(x3)	10	11	12	13
fdiv f3, f1, f7	11	12	22	23
fsub f6, f3, f4	14	24	26	27
fmul f7, f1, f2	15	16	20	21
fadd f4, f5, f2	28	29	31	32
fsd f1, 50(x11)	29	30	31	32
