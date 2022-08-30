# https://help.smarkets.com/hc/en-gb/articles/115001431011-How-to-calculate-a-hedge-bet

class Calculation:

    '''

    if the odds have shortened after an initial lay OR drifted after an initial back:
    we can hedge to Reduce the risk - called 'redding down' - lock in a loss
    Here, I want to perform calculations to see the total loss from redding up, and compare this to the total
    loss if I do NOT red up - ie let my initial lay or back come in (ie. if backed first, I would loose my
    initial stake. If layed first, I would loose my liability - so calculate liability) Once we have these two figures,
    print the Loss In Redding Down Vs Loss in Letting Bets Run ( EV if let bets run - Loss From Bet Running x Percentage Odds)
    Also want to have printed the instructions on how to do it

    if the odds have drifted after an initial lay OR shortened after an initial back:
    we can hedge to Lock in a profit, regardless of the outcome - called 'Greening Up'. This reduces our max
    we can earn if we let our bets run. Again, as above, we want too calculate the gains from greening up Vs the gains from
    letting the bets run, assuming the initial odds change is in our favour. (Calc the EV too - prob_winning X payout + prob_losing X liability?)

    '''

    def __init__(self, first_bet_type, stake):
        self.first_bet_type = first_bet_type
        self.initial_stake = stake
        self.initial_odds = None
        self.in_trade = None

        self.current_lay_odds = None
        self.current_back_odds = None
        self.hedge_strategy = None
        self.profit_lay = None
        self.profit_back = None

        self.stake_to_lay = None
        self.stake_to_back = None
        self.lay_liability = None

    def setInitialOdds(self, initial_odds):
        self.initial_odds = initial_odds

    def setCurrentOdds(self, current_lay_odds, current_back_odds):
        self.current_lay_odds = current_lay_odds
        self.current_back_odds = current_back_odds

    def red_or_green(self):
        if (self.first_bet_type == 'Back' and self.current_lay_odds < self.initial_odds) \
              or (self.first_bet_type == 'Lay' and self.current_back_odds > self.initial_odds):
            self.hedge_strategy = 'Green Up'
        else:
            self.hedge_strategy = 'Red Down'

    def pnlCalculator(self):
        curr_lay_odds = float(self.current_lay_odds)
        curr_back_odds = float(self.current_back_odds)

        prev_odds = float(self.initial_odds) # The odds we were matched at for our initial lay or back bet
        initial_stake = float(self.initial_stake)

        #Back To Lay Hedge Bet
        if self.first_bet_type == 'Back':
            lay_stake = prev_odds * initial_stake / curr_lay_odds
            back_stake = float(self.initial_stake)

            lay_liability = lay_stake * (curr_lay_odds - 1)

            profit_if_back_wins = initial_stake * prev_odds - lay_liability - initial_stake
            profit_if_lay_wins = lay_stake - initial_stake

            self.profit_lay = profit_if_lay_wins
            self.profit_back = profit_if_back_wins

        #Lay To Back Hedge Bet
        else:
            back_stake = prev_odds * initial_stake / curr_back_odds
            lay_stake = float(self.initial_stake)

            lay_liability = lay_stake * (prev_odds - 1)

            profit_if_back_wins = back_stake * curr_back_odds - lay_liability - back_stake
            profit_if_lay_wins = lay_stake - back_stake

            self.profit_lay = profit_if_lay_wins
            self.profit_back = profit_if_back_wins

        self.stake_to_back = back_stake
        self.stake_to_lay = lay_stake
        self.lay_liability = lay_liability


def CalculationPrompter(calc_object):

    hedger = calc_object
    ach_odds = input('Enter the Achieved Odds: ')
    hedger.setInitialOdds(ach_odds)

    curr_lay_odds, curr_back_odds = input('Current Market Lay Odds, and Back Odds (L, B): ').split(", ")

    hedger.setCurrentOdds(curr_lay_odds, curr_back_odds)

    hedger.pnlCalculator()

    if float(hedger.profit_lay) > 0 or float(hedger.profit_back) > 0:
        hedger.hedge_strategy = 'Green Up'
    else:
        hedger.hedge_strategy = 'Red Down'

    if hedger.hedge_strategy == 'Green Up':

        printing_logic(hedger)
        hedge_executed = input('Hedge Executed (Y/N)?: ')
        key_function(hedge_executed, hedger)

    else:
        printing_logic(hedger)
        hedge_executed = input('Hedge Executed (Y/N)?: ')
        key_function(hedge_executed, hedger)


def key_function(hedge_executed, hedger):
    if hedge_executed == 'Y':

        new_calc = input('Do you wish to do a new hedging calculation (Y / N)?: ')
        if new_calc == 'Y':
            master()
        else:
            print('+-------------------------------------------------------------------+')
            print('| Exited Calculation Mode. Re-Run Script For New Hedge Calculations |')
            print('+-------------------------------------------------------------------+')

    else:
        odds_moved = input('Have the current odds changed (Y/N)?: ')
        if odds_moved == 'Y': # A)
            data_collector(hedger, hedger.first_bet_type, hedger.initial_stake, hedger.initial_odds)
            printing_logic(hedger)
            hedge_executed = input('Hedge Executed (Y/N)?: ')
            key_function(hedge_executed, hedger)
        else:
            printing_logic(hedger)
            hedge_executed = input('Hedge Executed (Y/N)?: ')
            key_function(hedge_executed, hedger)
        new_calc = input('Do you wish to do a new hedging calculation (Y / N)?: ')

        if new_calc == 'Y':
            print('+-------------------------------------------------------------------+')
            print('|                          NEW CALCULATION                          |')
            print('+-------------------------------------------------------------------+')
            master()
        else:
            print('+-------------------------------------------------------------------+')
            print('| Exited Calculation Mode. Re-Run Script For New Hedge Calculations |')
            print('+-------------------------------------------------------------------+')


def data_collector(hedger, bet_type, stake, odds):
    updt_lay_odds, updt_back_odds = input('What are the current market lay odds, and back odds?: ').split(", ")
    hedger.setCurrentOdds(updt_lay_odds, updt_back_odds)
    hedger.pnlCalculator()


def print_calcs(hedger):
    print('---> {}'.format('Lay £ ' + str(round(hedger.stake_to_lay, 2)) if hedger.first_bet_type == 'Back' else
                           'Back £ ' + str(round(hedger.stake_to_back, 2))))
    print('\n')
    print('Maximum PnL without hedging is: {}'.format(
        float(hedger.initial_stake) * float(hedger.initial_odds) if hedger.first_bet_type == 'Back'
        else hedger.initial_stake))  # If our first bet type is a Lay, the most we receive is the stake
    print('Hedging Gives a {} % ROI, Compared to {} % ROI if Bet Goes in Your Favour'.format(
        (round(hedger.profit_back, 2) / float(hedger.initial_stake)) * 100 if hedger.first_bet_type == 'Back' else
        (round(hedger.profit_lay, 2) / float(hedger.initial_stake)) * 100,
        (round(float(hedger.initial_odds), 2) / float(
            hedger.initial_stake)) * 100 if hedger.first_bet_type == 'Back' else
        '100'))


def printing_logic(hedger):
    print('+-------------------------------------------------------------------+')
    print('This is a {} hedge'.format(hedger.hedge_strategy))
    print('+-------------------------------------------------------------------+')

    print('Complete The Following Order to Lock-In a PnL of £ {}, £ {}:'.format(round(hedger.profit_lay,2),
                                                                                round(hedger.profit_back,2)))
    print('\n')
    if hedger.hedge_strategy == 'Green Up':
        print_calcs(hedger)
    # When our first bet is a Lay, the ROI is the profit from hedging our lay / the initial stake received from offering our lay
    else:
        print('---> {}'.format('Lay £ ' + str(round(hedger.stake_to_lay, 2)) if hedger.first_bet_type == 'Back' else
                                'Back £ ' + str(round(hedger.stake_to_back, 2))))
        print('\n')
        print('Maximum PnL without hedging is: {}'.format(
            float(hedger.initial_stake) if hedger.first_bet_type == 'Back' else hedger.initial_stake * (hedger.initial_odds - 1) )) # If our first bet type is a Lay, the most we can loose is lay liability
        print('Hedging Gives Loss of {} % on Stake, Compared to {} % if Bet Goes Against You'.format(
            (round(hedger.profit_back, 2) / float(hedger.initial_stake)) * 100 if hedger.first_bet_type == 'Back' else
            (round(hedger.profit_lay, 2) / (float(hedger.initial_stake) * ( float(hedger.initial_odds) - 1)) ) * 100,
            '100' if hedger.first_bet_type == 'Back' else
            hedger.initial_odds * 100))
    print('+-------------------------------------------------------------------+')


def master():
    first_bet_type = input('Please Enter Type of First Bet (Lay / Back): ')

    if first_bet_type != 'Lay' or first_bet_type != 'Back':
        print('----------------------------------------------')
        print('Invalid Bet Type. Must be \'Lay\' or \'Back\'')
        print('----------------------------------------------')
        first_bet_type = input('Please Enter Type of First Bet (Lay / Back): ')

    stake = input('Please Enter Your Stake: ')
    hedge_calculator = Calculation(first_bet_type, stake)
    CalculationPrompter(hedge_calculator)

master()

#TODO: When implimenting this live, have an odds achieved variable as we may encounter slippage on the exchange.
# to get this, probably have to connect to the betfair API with your order etc.
