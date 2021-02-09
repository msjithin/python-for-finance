from random import randint

picks = ['Rock', 'Paper', 'Scissors']
score_1 = 0
score_2 = 0
#set player to False
player1 = False
while True:
    go_on = input('Play again! ')
    if len(go_on) == 0 :
        print('Scores : \n  You {}  \t Computer {} '.format(score_1, score_2))
        break
    print('Rock Paper or Scissors ? ')
    for i in range(len(picks)):
        print('[{}]  {}'.format(i+1, picks[i]))
    
    picked_index = input('Make selection : ')
    if picked_index not in ['1', '2', '3']:
        print('Select one of the options with 1,2, or 3')
        continue
    player1 = picks[int(picked_index)-1].lower()
    player2 = picks[randint(0,2)].lower()
    print('Selections....   Computer : {} , You : {} '.format(player2, player1))
    if player1 == player2 :
        print('Its a Tie! {} - {} '.format(player1, player2))
    elif player1 == 'rock':
        if player2 == 'paper':
            print('Computer wins! Paper covers Rock')
            score_2 += 1
        elif player2 == 'scissors':
            print('You win! Rock crushes Scissors')
            score_1 += 1
    elif player1 == 'paper':
        if player2 == 'rock':
            print('You win! Paper covers Rock')
            score_1 += 1
        elif player2 == 'scissors':
            print('Computer wins! Scissors cuts paper')
            score_2 += 1
    elif player1 == 'scissors':
        if player2 == 'paper':
            print('You win! Scissors cuts paper')
            score_1 += 1
        elif player2 == 'rock':
            print('Computer wins! Rock crushes Scissors')
            score_2 += 1
    else:
        print('Something is fishy')






