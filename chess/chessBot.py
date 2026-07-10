import copy
import random

test_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

files={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
ranks={'8':0,'7':1,'6':2,'5':3,'4':4,'3':5,'2':6,'1':7}
Rfiles={0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
Rranks={0:'8',1:'7',2:'6',3:'5',4:'4',5:'3',6:'2',7:'1'}

def board_to_pieces(board) :
    white_p=[]
    black_p=[]
    for i in range(len(board)) :
        for piece in board[i] :
            if piece!='-' :
                if piece.color=='white' :
                    white_p.append(piece)
                else :
                    black_p.append(piece)

    return white_p, black_p

def pieces_to_board(pieces) :
    board=[['-' for sq in range(8)] for sq in range(8)]
    for piece in pieces :
        board[piece.y][piece.x]=piece

    return board

def board_num_to_xy(board_num) :
    x=board_num%8
    y=board_num//8
    return [x,y]

def xy_to_board_num(x,y) :
    return (y*8)+x

def acn_to_xy(acn) :
    x=files[acn[0]]
    y=ranks[acn[1]]
    return x,y

def acn_to_board_num(acn) :
    x,y=acn_to_xy(acn)
    b_num=xy_to_board_num(x,y)
    return b_num

class Piece :
    def __init__(self,color,piece,x,y):
        self.color=color
        self.piece=piece
        self.x=x
        self.y=y
        if self.piece in ['pawn','rook','king'] :
            if self.piece in ['rook','king'] :
                self.can_castle=True
            if self.piece=='pawn' :
                self.start_y=1 if self.color=='black' else 6
        if self.piece=='knight' :
            self.piece_code='n'
        else :
            self.piece_code=self.piece[0]
        if self.color=='white' :
            self.piece_code=self.piece_code.upper()

    def get_pos(self) :
        return self.x+(self.y*8)


def fen_to_board(fen) :
    x,y=0,0
    sep_fen=fen.split()
    numbers='12345678'
    board_grid=[['-' for sq in range(8)] for sq in range(8)]
    for cell in range(len(sep_fen[0])) :
        if fen[cell]!=' ' :
            if fen[cell]=='k' :
                board_grid[y][x]=Piece('black','king',x,y)
                x+=1
            if fen[cell]=='q' :
                board_grid[y][x]=Piece('black','queen',x,y)
                x+=1
            if fen[cell]=='b' :
                board_grid[y][x]=Piece('black','bishop',x,y)
                x+=1
            if fen[cell]=='n' :
                board_grid[y][x]=Piece('black','knight',x,y)
                x+=1
            if fen[cell]=='r' :
                board_grid[y][x]=Piece('black','rook',x,y)
                x+=1
            if fen[cell]=='p' :
                board_grid[y][x]=Piece('black','pawn',x,y)
                x+=1

            if fen[cell]=='K' :
                board_grid[y][x]=Piece('white','king',x,y)
                x+=1
            if fen[cell]=='Q' :
                board_grid[y][x]=Piece('white','queen',x,y)
                x+=1
            if fen[cell]=='B' :
                board_grid[y][x]=Piece('white','bishop',x,y)
                x+=1
            if fen[cell]=='N' :
                board_grid[y][x]=Piece('white','knight',x,y)
                x+=1
            if fen[cell]=='R' :
                board_grid[y][x]=Piece('white','rook',x,y)
                x+=1
            if fen[cell]=='P' :
                board_grid[y][x]=Piece('white','pawn',x,y)
                x+=1

            if fen[cell] in numbers :
                for _ in range(int(fen[cell])) :
                    x+=1
            if fen[cell]=='/' :
                x=0
                y+=1
    if sep_fen[1]=='w' :
        turn='white'
    elif sep_fen[1]=='b' :
        turn='black'
    else :
        turn='test'
    
    castling_rights=[False,False,False,False]
    if sep_fen[2]!='-' :
        for right in sep_fen[2] :
            if right=='K' :
                castling_rights[0]=True
            elif right=='Q' :
                castling_rights[1]=True
            elif right=='k' :
                castling_rights[2]=True
            elif right=='q' :
                castling_rights[3]=True
            else :
                castling_rights=None

    if sep_fen[3]!='-' :
        en_passant=acn_to_board_num(sep_fen[3])
    else :
        en_passant=None

    movesForDraw=int(sep_fen[4])

    t_moves=int(sep_fen[5])

    return board_grid, turn, castling_rights, en_passant, movesForDraw, t_moves

def get_piece_at(square, pieces):
    x, y = board_num_to_xy(square)
    for p in pieces:
        if p.x == x and p.y == y:
            return p
    return None

def is_attacked(square, turn, w_pieces, b_pieces):
    rook_dirs = [-8, 8, -1, 1]
    bishop_dirs = [-9, -7, 7, 9]
    knight_dirs = [-17, -15, -10, -6, 6, 10, 15, 17]
    king_dirs = [-9, -8, -7, -1, 1, 7, 8, 9]
    enemy = b_pieces if turn == 'white' else w_pieces
    friendly = w_pieces if turn == 'white' else b_pieces
    sx, sy = board_num_to_xy(square)

    pawn_dir = -1 if turn == 'white' else 1
    for dx in (-1, 1):
        nx, ny = sx + dx, sy + pawn_dir
        if 0 <= nx < 8 and 0 <= ny < 8:
            p = get_piece_at(nx + ny * 8, enemy)
            if p and p.piece == 'pawn':
                return True

    for off in knight_dirs :
        sq = square + off
        if 0 <= sq < 64:
            x, y = board_num_to_xy(sq)
            if abs(x - sx) + abs(y - sy) == 3:
                p = get_piece_at(sq, enemy)
                if p and p.piece == 'knight':
                    return True

    for d in rook_dirs:
        sq = square + d
        while 0 <= sq < 64:
            x, y = board_num_to_xy(sq)
            if d in (-1, 1) and y != sy:
                break
            p = get_piece_at(sq, enemy + friendly)
            if p :
                if p in enemy and p.piece in ('rook', 'queen'):
                    return True
                break
            sq += d

    for d in bishop_dirs :
        sq = square + d
        while 0 <= sq < 64:
            x, y = board_num_to_xy(sq)
            if abs(x - sx) != abs(y - sy):
                break
            p = get_piece_at(sq, enemy + friendly)
            if p:
                if p in enemy and p.piece in ('bishop', 'queen'):
                    return True
                break
            sq += d

    for d in king_dirs:
        sq = square + d
        if 0 <= sq < 64:
            x, y = board_num_to_xy(sq)
            if abs(x - sx) <= 1 and abs(y - sy) <= 1:
                p = get_piece_at(sq, enemy)
                if p and p.piece == 'king':
                    return True

    return False
    
def get_legalMoves(pieceToMove,turn, white_pieces, black_pieces,en_passant_sq) :
    legal_squares=[]
    if turn in [pieceToMove.color,'test'] :
        enemy_pieces=black_pieces if pieceToMove.color=='white' else white_pieces
        friendly_pieces=white_pieces if pieceToMove.color=='white' else black_pieces
        temp_Wpieces,temp_Bpieces=copy.deepcopy(white_pieces),copy.deepcopy(black_pieces)
        if pieceToMove.piece=='pawn' :
            direction=-1 if pieceToMove.color=='white' else +1
            enemy_on_square=False
            friendly_on_square=False
            enemy_on_square_tl=False
            enemy_on_square_tr=False
            legal_move=pieceToMove.get_pos()+(8*direction)
            start_rank=6 if pieceToMove.color=='white' else 1

            if pieceToMove.y!=start_rank :
                for piece in enemy_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        enemy_on_square=True

                for piece in friendly_pieces :
                        if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                            friendly_on_square=True 

                if not enemy_on_square and not friendly_on_square and 0<=legal_move<=63 :
                    legal_squares.append(legal_move)

            else :
                for _ in range(2) :
                    enemy_on_square=False
                    friendly_on_square=False

                    for piece in enemy_pieces :
                        if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                            enemy_on_square=True

                    for piece in friendly_pieces :
                        if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                            friendly_on_square=True 

                    if friendly_on_square or enemy_on_square :
                        break

                    legal_squares.append(legal_move)
                    legal_move=legal_move+(8*direction)

                legal_move=pieceToMove.get_pos()+(8*direction)

            for piece in enemy_pieces :
                if piece.x==board_num_to_xy(legal_move+1)[0] and piece.y==board_num_to_xy(legal_move+1)[1] and (legal_move+1)//8==legal_move//8 :
                    enemy_on_square_tl=True
                if piece.x==board_num_to_xy(legal_move-1)[0] and piece.y==board_num_to_xy(legal_move-1)[1] and (legal_move-1)//8==legal_move//8 :
                    enemy_on_square_tr=True

            if enemy_on_square_tl :
                legal_squares.append(legal_move+1)
            if enemy_on_square_tr :
                legal_squares.append(legal_move-1)
            
            if en_passant_sq is not None:
                if abs(en_passant_sq - pieceToMove.get_pos()) in (7, 9):
                    legal_squares.append(en_passant_sq)

            filtered_moves=[]
            for move in legal_squares :
                temp_enemy_pieces=temp_Bpieces if pieceToMove.color=='white' else temp_Wpieces
                temp_friendly_pieces=temp_Wpieces if pieceToMove.color=='white' else temp_Bpieces
                piece=next(p for p in temp_friendly_pieces if p.x==pieceToMove.x and p.y==pieceToMove.y and p.color==pieceToMove.color and p.piece==pieceToMove.piece)
                piece.x,piece.y=board_num_to_xy(move)
                for a_piece in temp_enemy_pieces :
                    if a_piece.x==piece.x and a_piece.y==piece.y :
                        temp_enemy_pieces.remove(a_piece)
                king = next(p for p in temp_friendly_pieces if p.piece == 'king')
                king_sq = xy_to_board_num(king.x, king.y)
                if not is_attacked(king_sq,turn,temp_Wpieces,temp_Bpieces) :
                    filtered_moves.append(move)
                temp_Wpieces,temp_Bpieces=copy.deepcopy(white_pieces),copy.deepcopy(black_pieces)
            legal_squares=filtered_moves

        if pieceToMove.piece in ['rook','queen'] :
            enemy_on_square=False
            friendly_on_square=False

            legal_move=pieceToMove.get_pos()-8
            while legal_move>=0 :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                        break

                for piece in enemy_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        enemy_on_square=True
                        break

                if friendly_on_square :
                    break

                legal_squares.append(legal_move)
                legal_move=legal_move-8

                if enemy_on_square :
                    break

            legal_move=pieceToMove.get_pos()+8
            while legal_move<64 :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                        break
                    
                for piece in enemy_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        enemy_on_square=True
                        break

                if friendly_on_square :
                    break

                legal_squares.append(legal_move)
                legal_move=legal_move+8

                if enemy_on_square :
                    break

            legal_move=pieceToMove.get_pos()-1
            while legal_move>=0 and legal_move//8==pieceToMove.y :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True

                for piece in enemy_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        enemy_on_square=True
                        break

                if friendly_on_square :
                    break

                legal_squares.append(legal_move)
                legal_move=legal_move-1

                if enemy_on_square :
                    break


            legal_move=pieceToMove.get_pos()+1
            while legal_move<64 and legal_move//8==pieceToMove.y :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                            
                for piece in enemy_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        enemy_on_square=True
                        break

                if friendly_on_square :
                    break

                legal_squares.append(legal_move)
                legal_move=legal_move+1

                if enemy_on_square :
                    break

            filtered_moves=[]
            for move in legal_squares :
                temp_enemy_pieces=temp_Bpieces if pieceToMove.color=='white' else temp_Wpieces
                temp_friendly_pieces=temp_Wpieces if pieceToMove.color=='white' else temp_Bpieces
                piece=next(p for p in temp_friendly_pieces if p.x==pieceToMove.x and p.y==pieceToMove.y and p.color==pieceToMove.color and p.piece==pieceToMove.piece)
                piece.x,piece.y=board_num_to_xy(move)
                for a_piece in temp_enemy_pieces :
                    if a_piece.x==piece.x and a_piece.y==piece.y :
                        temp_enemy_pieces.remove(a_piece)
                king = next(p for p in temp_friendly_pieces if p.piece == 'king')
                king_sq = xy_to_board_num(king.x, king.y)
                if not is_attacked(king_sq,turn,temp_Wpieces,temp_Bpieces) :
                    filtered_moves.append(move)
                temp_Wpieces,temp_Bpieces=copy.deepcopy(white_pieces),copy.deepcopy(black_pieces)
            legal_squares=filtered_moves

        if pieceToMove.piece in ['bishop','queen'] :
            enemy_on_square=False
            friendly_on_square=False

            legal_move=pieceToMove.get_pos()-9
            offset=1
            while legal_move>=0 and legal_move//8==pieceToMove.y-offset :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                        break

                for piece in enemy_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        enemy_on_square=True
                        break

                if friendly_on_square :
                    break

                legal_squares.append(legal_move)
                legal_move=legal_move-9
                offset+=1

                if enemy_on_square :
                    break

            legal_move=pieceToMove.get_pos()+9
            offset=1
            while legal_move<64 and legal_move//8==pieceToMove.y+offset :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                        break
                    
                for piece in enemy_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        enemy_on_square=True
                        break

                if friendly_on_square :
                    break

                legal_squares.append(legal_move)
                legal_move=legal_move+9
                offset+=1

                if enemy_on_square :
                    break

            legal_move=pieceToMove.get_pos()-7
            offset=1
            while legal_move>=0 and legal_move//8==pieceToMove.y-offset :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True

                for piece in enemy_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        enemy_on_square=True
                        break

                if friendly_on_square :
                    break

                legal_squares.append(legal_move)
                legal_move=legal_move-7
                offset+=1

                if enemy_on_square :
                    break


            legal_move=pieceToMove.get_pos()+7
            offset=1
            while legal_move<64 and legal_move//8==pieceToMove.y+offset :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                            
                for piece in enemy_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        enemy_on_square=True
                        break

                if friendly_on_square :
                    break

                legal_squares.append(legal_move)
                legal_move=legal_move+7
                offset+=1

                if enemy_on_square :
                    break

            filtered_moves=[]
            for move in legal_squares :
                temp_enemy_pieces=temp_Bpieces if pieceToMove.color=='white' else temp_Wpieces
                temp_friendly_pieces=temp_Wpieces if pieceToMove.color=='white' else temp_Bpieces
                piece=next(p for p in temp_friendly_pieces if p.x==pieceToMove.x and p.y==pieceToMove.y and p.color==pieceToMove.color and p.piece==pieceToMove.piece)
                piece.x,piece.y=board_num_to_xy(move)
                for a_piece in temp_enemy_pieces :
                    if a_piece.x==piece.x and a_piece.y==piece.y :
                        temp_enemy_pieces.remove(a_piece)
                king = next(p for p in temp_friendly_pieces if p.piece == 'king')
                king_sq = xy_to_board_num(king.x, king.y)
                if not is_attacked(king_sq,turn,temp_Wpieces,temp_Bpieces) :
                    filtered_moves.append(move)
                temp_Wpieces,temp_Bpieces=copy.deepcopy(white_pieces),copy.deepcopy(black_pieces)
            legal_squares=filtered_moves

        if pieceToMove.piece=='king' :
            legal_move=pieceToMove.get_pos()-8
            if legal_move>=0 :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                            
                if not friendly_on_square and not is_attacked(legal_move,turn,white_pieces,black_pieces) :
                    legal_squares.append(legal_move)

            legal_move=pieceToMove.get_pos()+8
            if legal_move<64 :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                            
                if not friendly_on_square and not is_attacked(legal_move,turn,white_pieces,black_pieces) :
                    legal_squares.append(legal_move)

            legal_move=pieceToMove.get_pos()-1
            if legal_move>=0 and legal_move//8==pieceToMove.y :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                            
                if not friendly_on_square and not is_attacked(legal_move,turn,white_pieces,black_pieces) :
                    legal_squares.append(legal_move)
                   
            legal_move=pieceToMove.get_pos()+1
            if legal_move<64 and legal_move//8==pieceToMove.y :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                            
                if not friendly_on_square and not is_attacked(legal_move,turn,white_pieces,black_pieces) :
                    legal_squares.append(legal_move)
                   
            legal_move=pieceToMove.get_pos()-9
            if legal_move>=0 and legal_move//8==pieceToMove.y-1 :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                            
                if not friendly_on_square and not is_attacked(legal_move,turn,white_pieces,black_pieces) :
                    legal_squares.append(legal_move)
                   
            legal_move=pieceToMove.get_pos()+9
            if legal_move<64 and legal_move//8==pieceToMove.y+1 :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                            
                if not friendly_on_square and not is_attacked(legal_move,turn,white_pieces,black_pieces) :
                    legal_squares.append(legal_move)
                   
            legal_move=pieceToMove.get_pos()-7
            if legal_move>=0 and legal_move//8==pieceToMove.y-1 :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                            
                if not friendly_on_square and not is_attacked(legal_move,turn,white_pieces,black_pieces) :
                    legal_squares.append(legal_move)
                   
            legal_move=pieceToMove.get_pos()+7
            if legal_move<64 and legal_move//8==pieceToMove.y+1 :
                enemy_on_square=False
                friendly_on_square=False
                for piece in friendly_pieces :
                    if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                        friendly_on_square=True
                            
                if not friendly_on_square and not is_attacked(legal_move,turn,white_pieces,black_pieces) :
                    legal_squares.append(legal_move)

            castling1=62 if pieceToMove.color=='white' else 6
            castling2=58 if pieceToMove.color=='white' else 2
            rook_y=7 if pieceToMove.color=='white' else 0
            if pieceToMove.can_castle :
                for rook in friendly_pieces :
                    if rook.piece=='rook' :
                        piece_in_middle=False
                        is_check=False
                        if rook.x==7 and rook.y==rook_y and rook.can_castle :
                            for piece_x in range(pieceToMove.x+1,rook.x) :
                                for piece in friendly_pieces+enemy_pieces :
                                    if piece.x==piece_x and piece.y==rook_y :
                                        piece_in_middle=True
                            for square in range(pieceToMove.get_pos(),xy_to_board_num(rook.x,rook.y)+1) :
                                if is_attacked(square,turn,white_pieces,black_pieces) :
                                    is_check=True

                            if not piece_in_middle and not is_check :
                                legal_squares.append(castling1)

                        piece_in_middle=False
                        is_check=False
                        if rook.x==0 and rook.y==rook_y and rook.can_castle :
                            for piece_x in range(pieceToMove.x-1,rook.x,-1) :
                                for piece in friendly_pieces+enemy_pieces :
                                    if piece.x==piece_x and piece.y==rook_y :
                                        piece_in_middle=True
                            for square in range(pieceToMove.get_pos(),xy_to_board_num(rook.x,rook.y)-1,-1) :
                                if is_attacked(square,turn,white_pieces,black_pieces) :
                                    is_check=True
                            if not piece_in_middle and not is_check :
                                legal_squares.append(castling2)

            filtered_moves=[]
            for move in legal_squares :
                temp_enemy_pieces=temp_Bpieces if pieceToMove.color=='white' else temp_Wpieces
                temp_friendly_pieces=temp_Wpieces if pieceToMove.color=='white' else temp_Bpieces
                piece=next(p for p in temp_friendly_pieces if p.x==pieceToMove.x and p.y==pieceToMove.y and p.color==pieceToMove.color and p.piece==pieceToMove.piece)
                piece.x,piece.y=board_num_to_xy(move)
                for a_piece in temp_enemy_pieces :
                    if a_piece.x==piece.x and a_piece.y==piece.y :
                        temp_enemy_pieces.remove(a_piece)
                king = next(p for p in temp_friendly_pieces if p.piece == 'king')
                king_sq = xy_to_board_num(king.x, king.y)
                if not is_attacked(king_sq,turn,temp_Wpieces,temp_Bpieces) :
                    filtered_moves.append(move)
                temp_Wpieces,temp_Bpieces=copy.deepcopy(white_pieces),copy.deepcopy(black_pieces)
            legal_squares=filtered_moves

        if pieceToMove.piece=='knight' :
            for y in [8,-8] :
                for x in [1,-1] :
                    legal_move=pieceToMove.get_pos()+x+(2*y)
                    friendly_on_square=False
                    valid_move=False

                    for piece in friendly_pieces :
                        if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                            friendly_on_square=True

                    if legal_move%8 in range(pieceToMove.x-1,pieceToMove.x+2,2) :
                        valid_move=True


                    if not friendly_on_square and 0<=legal_move<=63 and valid_move :
                        legal_squares.append(legal_move)

            for x in [1,-1] :
                for y in [8,-8] :
                    legal_move=pieceToMove.get_pos()+(2*x)+y
                    friendly_on_square=False
                    valid_move=False

                    for piece in friendly_pieces :
                        if piece.x==board_num_to_xy(legal_move)[0] and piece.y==board_num_to_xy(legal_move)[1] :
                            friendly_on_square=True

                    if legal_move//8 in range(pieceToMove.y-1,pieceToMove.y+2,2) :
                        valid_move=True

                    if not friendly_on_square and 0<=legal_move<=63 and valid_move :
                        legal_squares.append(legal_move)

            filtered_moves=[]
            for move in legal_squares :
                temp_enemy_pieces=temp_Bpieces if pieceToMove.color=='white' else temp_Wpieces
                temp_friendly_pieces=temp_Wpieces if pieceToMove.color=='white' else temp_Bpieces
                piece=next(p for p in temp_friendly_pieces if p.x==pieceToMove.x and p.y==pieceToMove.y and p.color==pieceToMove.color and p.piece==pieceToMove.piece)
                piece.x,piece.y=board_num_to_xy(move)
                for a_piece in temp_enemy_pieces :
                    if a_piece.x==piece.x and a_piece.y==piece.y :
                        temp_enemy_pieces.remove(a_piece)
                king = next(p for p in temp_friendly_pieces if p.piece == 'king')
                king_sq = xy_to_board_num(king.x, king.y)
                if not is_attacked(king_sq,turn,temp_Wpieces,temp_Bpieces) :
                    filtered_moves.append(move)
                temp_Wpieces,temp_Bpieces=copy.deepcopy(white_pieces),copy.deepcopy(black_pieces)
            legal_squares=filtered_moves

    return legal_squares

class ChessAI :
    def __init__(self):
        self.queen_val=9
        self.rook_val=5
        self.knight_val=3
        self.bishop_val=3
        self.pawn_val=1

    def load_board(self,fen) :
        self.board, self.turn, self.castling_rights, self.en_passant_sq, self.moves_since_pm_or_c, self.total_moves=fen_to_board(fen)
        self.w_pieces, self.b_pieces=board_to_pieces(self.board)

    def get_all_legal_moves(self) :
        legal_moves:list[list[list[int]]]=[]
        for piece in self.w_pieces+self.b_pieces :
            piece_legal_moves=get_legalMoves(piece,self.turn,self.w_pieces,self.b_pieces,self.en_passant_sq)
            sx, sy=piece.x, piece.y
            for move in piece_legal_moves :
                ex, ey=board_num_to_xy(move)
                legal_moves.append([[sx,sy],[ex,ey]])

        return legal_moves
    
    def move_to_uci(self,move) :
        start_xy=move[0]
        end_xy=move[1]
        uci1=Rfiles[start_xy[0]]
        uci2=Rranks[start_xy[1]]
        uci3=Rfiles[end_xy[0]]
        uci4=Rranks[end_xy[1]]
        uci=uci1+uci2+uci3+uci4
        return uci
    
    def select_move(self) :
        legalMoves=self.get_all_legal_moves()
        if legalMoves :
            move=random.choice(legalMoves)
            uci_move=self.move_to_uci(move)
        else :
            uci_move=None
        return uci_move
    
    def get_promoted_piece(self) :
        return 'queen'
    

