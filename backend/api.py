from flask import Flask, request, jsonify
from models import Session, Trader, Leaderboard, Staking

app = Flask(__name__)
session = Session()


@app.route('/traders', methods=['GET'])
def get_traders():
    min_win_rate = request.args.get('min_win_rate', default=0, type=float)
    traders = session.query(Trader).filter(
        Trader.win_rate >= min_win_rate).all()
    return jsonify([trader.name for trader in traders])


@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    leaderboard = session.query(Leaderboard).order_by(Leaderboard.rank).all()
    return jsonify([{'name': lb.trader.name, 'rank': lb.rank} for lb in leaderboard])


@app.route('/stake', methods=['POST'])
def stake():
    data = request.json
    new_stake = Staking(user_id=data['user_id'],
                        amount_staked=data['amount'], reward=0)
    session.add(new_stake)
    session.commit()
    return jsonify({'message': 'Staked successfully'})


if __name__ == '__main__':
    app.run(debug=True)
