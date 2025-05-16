import TicTacToe as ttt

def main():

	# Players
	rlAgent = ttt.createPlayer('X', ttt.RL_AGENT)
	rlAgent.name = 'Alice'

	partner = ttt.createPlayer('O', ttt.RANDOM_AGENT)
	partner.name = "Random"

	# Training Session
	rlAgent.initTraining(0.1, 0.2, 0.3)
	ttt.train(rlAgent, partner, 500)

	# Evaluation
	rlAgent.setMode(ttt.PLAYING_MODE)
	tournament = ttt.Tournament()
	tournament.start(rlAgent, partner, 5)
	tournament.start(partner, rlAgent, 5)
	tournament.printStats([rlAgent, partner])

main()
