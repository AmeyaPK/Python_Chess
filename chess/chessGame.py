import pygame
import sys
import copy
import chessBot

files={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
ranks={'8':0,'7':1,'6':2,'5':3,'4':4,'3':5,'2':6,'1':7}
Rfiles={0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
Rranks={0:'8',1:'7',2:'6',3:'5',4:'4',5:'3',6:'2',7:'1'}





        
class Piece :
    def __init__(self,color,piece,x,y):
        self.color=color
        self.piece=piece
        self.x=x
        self.y=y
        self.piece_x=(self.x*cell_size)+board_x+cell_size/2
        self.piece_y=(self.y*cell_size)+board_y+cell_size/2
        if self.piece in ['pawn','rook','king'] :
            if self.piece in ['rook','king'] :
                self.can_castle=True
                if self.piece=='rook' :
                    self.start_x=self.x
            if self.piece=='pawn' :
                self.start_y=1 if self.color=='black' else 6
        if self.piece=='knight' :
            self.piece_code='n'
        else :
            self.piece_code=self.piece[0]
        if self.color=='white' :
            self.piece_code=self.piece_code.upper()

    def draw_piece(self) :
        piece_images={
            ('white','king'):white_king,
            ('white','queen'):white_queen,
            ('white','bishop'):white_bishop,
            ('white','knight'):white_knight,
            ('white','rook'):white_rook,
            ('white','pawn'):white_pawn,
            ('black','king'):black_king,
            ('black','queen'):black_queen,
            ('black','bishop'):black_bishop,
            ('black','knight'):black_knight,
            ('black','rook'):black_rook,
            ('black','pawn'):black_pawn
        }
        self.piece_surf=piece_images[(self.color,self.piece)]
        pygame.transform.smoothscale(self.piece_surf, (cell_size,cell_size))
        self.piece_rect=self.piece_surf.get_rect(center=(self.piece_x,self.piece_y))
        screen.blit(self.piece_surf, self.piece_rect)

    def update_piece_pixel_pos(self):
        self.piece_x = board_x + self.x * cell_size + cell_size//2
        self.piece_y = board_y + self.y * cell_size + cell_size//2

    def get_pos(self) :
        return self.x+(self.y*8)

    def update_info(self) :
        if self.piece in ['pawn','rook','king'] :
            if self.piece in ['rook','king'] :
                self.can_castle=True
                if self.piece=='rook' :
                    self.start_x=self.x
            if self.piece=='pawn' :
                self.start_y=1 if self.color=='black' else 6
        if self.piece=='knight' :
            self.piece_code='n'
        else :
            self.piece_code=self.piece[0]
        if self.color=='white' :
            self.piece_code=self.piece_code.upper()



class Button :
    def __init__(self,x,y,w,h,type,text = None,font_size = None,text_color = None,img = None) :
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.type = type
        self.img=img
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.pressed=False
        self.button_bgRect=pygame.Rect(self.x,self.y,self.w,self.h)

    def drawButton(self,bg_color,hover_color) :
        m_pos=pygame.mouse.get_pos()
        if self.button_bgRect.collidepoint(m_pos) :
            b_color=hover_color
        else :
            b_color=bg_color
        if self.type == "img":
            button_surface=self.img
            button_rect=button_surface.get_rect(center=(self.button_bgRect.centerx,self.button_bgRect.centery))
            pygame.draw.rect(screen,b_color,self.button_bgRect)
            screen.blit(button_surface,button_rect)
        elif self.type == "text":
            drawTitle(self.font_size, self.x, self.y, self.w, self.h, b_color, self.text_color, self.text, "center", 0, 0)

    def is_clicked(self) :
        m_pos=pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]==1 and self.button_bgRect.collidepoint(m_pos) :
            self.pressed=True
        if pygame.mouse.get_pressed()[0]==0 and self.button_bgRect.collidepoint(m_pos) and self.pressed :
            self.pressed=False
            return True
        return False



class ask_draw_box:
    def __init__(self):
        self.width = 400
        self.height = 50
        self.x = 250
        self.y = 0
        self.offerer = None
        self.button_y_off = 10
        self.draw_offer_time = 0
        

    def ask_draw(self, color):
        self.draw_offer_time = draw_time
        self.offerer = color
        if color == "white":
            self.y = 895
        else:
            self.y = 15
        self.accept_button = Button(415, self.y + self.button_y_off, 100, 30, type="text", text="Accept", text_color="#FFF1F1", font_size=24)
        self.reject_button = Button(530, self.y + self.button_y_off, 100, 30, type="text", text="Reject", text_color="#F1FFF6", font_size=24)

    def draw(self):
        if self.offerer:
            drawTitle(24, self.x, self.y, self.width, self.height, "#ffffff", "#333333", self.offerer + " would like to\noffer a draw", "left", 5, 0)
            self.accept_button.drawButton("#E74646", "#FF8888")
            self.reject_button.drawButton("#48D46B", "#9AFFA7")

    def get_result(self):
        if self.accept_button.is_clicked():
            return True
        elif self.reject_button.is_clicked():
            return False
        return "in_progress"





def draw_board(board_x,board_y) :
    for x in range(cell_number) :
        for y in range(cell_number) :
            if x%2==0 and y%2==0 :
                cell_surf=pygame.Surface((cell_size,cell_size))
                cell_surf.fill(("#eeeed2"))
            elif x%2==0 and y%2!=0 :
                cell_surf=pygame.Surface((cell_size,cell_size))
                cell_surf.fill(("#769656"))
            elif x%2!=0 and y%2==0 :
                cell_surf=pygame.Surface((cell_size,cell_size))
                cell_surf.fill(("#769656"))
            elif x%2!=0 and y%2!=0 :
                cell_surf=pygame.Surface((cell_size,cell_size))
                cell_surf.fill(("#eeeed2"))
            screen.blit(cell_surf,((x*cell_size)+board_x,(y*cell_size)+board_y))


def drawTitle(fontSize,x,y,bgW,bgH,bgColor,textColor,text, text_pos, x_off, y_off) :
    titleFont=pygame.font.Font(None, fontSize)
    title_bgRect=pygame.Rect(x,y,bgW,bgH)
    title_surface=titleFont.render(text, True, textColor)
    if text_pos == "center":
        title_rect=title_surface.get_rect(center=(title_bgRect.center[0]+x_off, title_bgRect.center[1]+y_off))
    elif text_pos == "left":
        title_rect=title_surface.get_rect(midleft=(title_bgRect.midleft[0]+x_off, title_bgRect.midleft[1]+y_off))
    elif text_pos == "right":
            title_rect=title_surface.get_rect(midright=(title_bgRect.midright[0]+x_off, title_bgRect.midright[1]+y_off))
    pygame.draw.rect(screen,bgColor,title_bgRect)
    screen.blit(title_surface,title_rect)


def set_board(fen) :
    board, turn, castling_rights, en_passant_sq, moves_since_pm_or_c, total_moves = fen_to_board(fen)
    w_pieces, b_pieces = board_to_pieces(board)

    if turn=='white' :
        player_num = 0
    else :
        player_num = 1

    for piece in b_pieces+w_pieces :
        if piece.piece=='rook' :
            if piece.color == 'white' :
                if piece.start_x==7 :
                    piece.can_castle=castling_rights[0]
                if piece.start_x==0 :
                    piece.can_castle=castling_rights[1]
            if piece.color == 'black' :
                if piece.start_x==7 :
                    piece.can_castle=castling_rights[2]
                if piece.start_x==0 :
                    piece.can_castle=castling_rights[3]
        if piece.piece=='king' :
            if piece.color == 'white' :
                piece.can_castle = True if any([castling_rights[0], castling_rights[1]]) else False
            if piece.color == 'black' :
                piece.can_castle = True if any([castling_rights[2], castling_rights[3]]) else False

    return board, turn, en_passant_sq, moves_since_pm_or_c, total_moves, player_num, w_pieces, b_pieces


def acn_to_xy(acn) :
    x=files[acn[0]]
    y=ranks[acn[1]]
    return x,y


def acn_to_board_num(acn) :
    x,y=acn_to_xy(acn)
    b_num=xy_to_board_num(x,y)
    return b_num


def board_num_to_acn(move) :
    x,y=board_num_to_xy(move)
    acn1=Rfiles[x]
    acn2=Rranks[y]
    acn=acn1+acn2
    return acn


def fen_to_board(fen) :
    x,y=0,0
    sep_fen=fen.split()
    numbers='12345678'
    board_grid=[['-' for _ in range(8)] for _ in range(8)]
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

    if sep_fen[3]!='-' :
        en_passant=acn_to_board_num(sep_fen[3])
    else :
        en_passant=None

    movesForDraw=int(sep_fen[4])

    t_moves=int(sep_fen[5])

    return board_grid, turn, castling_rights, en_passant, movesForDraw, t_moves


def board_to_fen(board, turn, castling, en_passant, d_moves, t_moves) :
    fen=''
    empty=0
    for y in range(len(board)-1) :
        for x in range(len(board[y])) :
            if board[y][x]!='-' :
                if empty!=0 :
                    fen+=str(empty)
                fen+=board[y][x].piece_code
                empty=0
            else :
                empty+=1
        if empty!=0 :
            fen+=str(empty)
        empty=0
        fen+='/'
    for x in range(len(board[-1])) :
        if board[-1][x]!='-' :
            if empty!=0 :
                fen+=str(empty)
            fen+=board[-1][x].piece_code
            empty=0
        else :
            empty+=1
    if empty!=0 :
        fen+=str(empty)
    empty=0
    fen+=' '+turn[0]
    castling_r=' '
    if any(castling) :
        for right in range(len(castling)) :
            if castling[right] :
                if right==0 :
                    castling_r+='K'
                if right==1 :
                    castling_r+='Q'
                if right==2 :
                    castling_r+='k'
                if right==3 :
                    castling_r+='q'
    else :
        castling_r+=('-')
    fen+=castling_r
    if en_passant :
        fen+=' '+board_num_to_acn(en_passant)
    else :
        fen+=' -'
    fen+=' '+str(d_moves)
    fen+=' '+str(t_moves)

    return fen


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
    board=[['-' for _ in range(8)] for _ in range(8)]
    for piece in pieces :
        board[piece.y][piece.x]=piece

    return board


def board_num_to_xy(board_num) :
    x=board_num%8
    y=board_num//8
    return x,y


def xy_to_board_num(x,y) :
    return (y*8)+x


def update_piece_pos(piece) :
    m_pos=pygame.mouse.get_pos()
    piece.draw_piece()
    if pygame.mouse.get_pressed()[0] and piece.piece_rect.collidepoint(m_pos) :
        piece.piece_x=m_pos[0]
        piece.piece_y=m_pos[1]


def highlight_legalMoves(legalMoves) :
    for square in legalMoves :
        square_pos=board_num_to_xy(square)
        screen.blit(highlighter,((square_pos[0]*cell_size)+board_x,(square_pos[1]*cell_size)+board_y))


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

    
def get_legalMoves(pieceToMove,turn) :
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

        if pieceToMove.piece == 'knight':
            offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
            for off in offsets:
                sq = pieceToMove.get_pos() + off
                if 0 <= sq < 64:
                    nx, ny = board_num_to_xy(sq)
                    if abs(nx - pieceToMove.x) + abs(ny - pieceToMove.y) == 3:
                        if not get_piece_at(sq, friendly_pieces):
                            legal_squares.append(sq)

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


def is_game_end(turn,b_pieces,w_pieces,time,is_Bresign, is_Wresign, all_positions, is_draw) :
    friendly_pieces=w_pieces if turn=='white' else b_pieces
    is_position_repeated_three_times = False
    position_frequency = {}

    for position in all_positions :
        pos = position.split()[0]
        if pos in list(position_frequency.keys()) :
            position_frequency[pos] += 1
        else :
            position_frequency.setdefault(pos, 1)

    if 3 in list(position_frequency.values()) :
        is_position_repeated_three_times = True

    if len(b_pieces+w_pieces)==2 or moves_since_pm_or_c>=50 or is_position_repeated_three_times or is_draw == True :
        return 'draw'
    
    if time<=0 :
        return 'time'
    
    if is_Wresign :
        return 'w_win'
    
    if is_Bresign :
        return 'b_win'

    for piece in friendly_pieces :
        if piece.piece=='king' :
            king_sq=xy_to_board_num(piece.x,piece.y)
        legal=get_legalMoves(piece, turn)
        if legal!=[] :
            return False
        
    if is_attacked(king_sq,turn,w_pieces,b_pieces) :
        return 'checkmate'
    else :
        return 'stalemate'

    
def get_bot_input(uci,pieces) :
    startX=files[uci[0]]
    startY=ranks[uci[1]]
    endX=files[uci[2]]
    endY=ranks[uci[3]]
    startPos=xy_to_board_num(startX,startY)
    endPos=xy_to_board_num(endX,endY)
    for piece in pieces :
        if piece.get_pos()==startPos :
            return piece, startX, startY, startPos, endX, endY, endPos
    return None,None,None,None,None,None,None
    




cell_size=100
cell_number=8
grid_size=960
board_x=25
board_y=80
selected_piece=None
player=['white','black']
player_num=0
turn=player[player_num]
squares=[]
total_moves=1
total_halfmoves=2
moves_since_pm_or_c=0
en_passant_sq=None
en_passant_found=0
highlighter=pygame.Surface((cell_size,cell_size), pygame.SRCALPHA)
highlighter.fill((240, 230, 140, 150))
check_highlighter=pygame.Surface((cell_size,cell_size), pygame.SRCALPHA)
check_highlighter.fill((255, 0, 0, 150))
captured=False
castled=False
promoted=False
promotion_active=False
bot_has_moved = False
game_end=False
can_play=False
black_play_time=300
white_play_time=300
play_time_increment=0
black_time=black_play_time
white_time=white_play_time
time_increment=play_time_increment
is_Wresign=False
is_Bresign=False
positions=["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"]
draw_asked = False
draw_result = False
draw_time = 30

white='user'
black='user'

my_bot=chessBot.ChessAI()
bot1_color='white' if white=='bot' else None
bot2_color='black' if black=='bot' else None

white_pieces=[Piece('white','king',4,7),Piece('white','queen',3,7),Piece('white','bishop',2,7),Piece('white','bishop',5,7),Piece('white','knight',1,7),Piece('white','knight',6,7),Piece('white','rook',0,7),Piece('white','rook',7,7),Piece('white','pawn',0,6),Piece('white','pawn',1,6),Piece('white','pawn',2,6),Piece('white','pawn',3,6),Piece('white','pawn',4,6),Piece('white','pawn',5,6),Piece('white','pawn',6,6),Piece('white','pawn',7,6)]
black_pieces=[Piece('black','king',4,0),Piece('black','queen',3,0),Piece('black','bishop',2,0),Piece('black','bishop',5,0),Piece('black','knight',1,0),Piece('black','knight',6,0),Piece('black','rook',0,0),Piece('black','rook',7,0),Piece('black','pawn',0,1),Piece('black','pawn',1,1),Piece('black','pawn',2,1),Piece('black','pawn',3,1),Piece('black','pawn',4,1),Piece('black','pawn',5,1),Piece('black','pawn',6,1),Piece('black','pawn',7,1)]
start_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
board, turn, en_passant_sq, moves_since_pm_or_c, total_moves, player_num, white_pieces, black_pieces = set_board(start_fen)

for y in range(len(board)) :
    for x in board[y] :
        code=x.piece_code if x!='-' else '-'
        print(code,end=' ')
    print()





pygame.init()
screen=pygame.display.set_mode((grid_size,grid_size))
clock=pygame.time.Clock()

white_king=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/white-king.png").convert_alpha()
white_queen=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/white-queen.png").convert_alpha()
white_bishop=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/white-bishop.png").convert_alpha()
white_knight=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/white-knight.png").convert_alpha()
white_rook=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/white-rook.png").convert_alpha()
white_pawn=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/white-pawn.png").convert_alpha()
black_king=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/black-king.png").convert_alpha()
black_queen=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/black-queen.png").convert_alpha()
black_bishop=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/black-bishop.png").convert_alpha()
black_knight=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/black-knight.png").convert_alpha()
black_rook=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/black-rook.png").convert_alpha()
black_pawn=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/pieces/black-pawn.png").convert_alpha()
undo_move_img=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/undo-move.png").convert_alpha()
restart_img=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/restart.png").convert_alpha()
resign_img=pygame.image.load("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/images/resign.png").convert_alpha()

pygame.transform.smoothscale(white_king, (cell_size,cell_size))
pygame.transform.smoothscale(white_queen, (cell_size,cell_size))
pygame.transform.smoothscale(white_bishop, (cell_size,cell_size))
pygame.transform.smoothscale(white_knight, (cell_size,cell_size))
pygame.transform.smoothscale(white_rook, (cell_size,cell_size))
pygame.transform.smoothscale(white_pawn, (cell_size,cell_size))
pygame.transform.smoothscale(black_king, (cell_size,cell_size))
pygame.transform.smoothscale(black_queen, (cell_size,cell_size))
pygame.transform.smoothscale(black_bishop, (cell_size,cell_size))
pygame.transform.smoothscale(black_knight, (cell_size,cell_size))
pygame.transform.smoothscale(black_rook, (cell_size,cell_size))
pygame.transform.smoothscale(black_pawn, (cell_size,cell_size))


move_sound=pygame.mixer.Sound("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/audio/move-self.mp3")
check_sound=pygame.mixer.Sound("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/audio/move-check.mp3")
capture_sound=pygame.mixer.Sound("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/audio/capture.mp3")
promote_sound=pygame.mixer.Sound("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/audio/promote.mp3")
castle_sound=pygame.mixer.Sound("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/audio/castle.mp3")
game_start_sound=pygame.mixer.Sound("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/audio/game-start.mp3")
game_end_sound=pygame.mixer.Sound("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/audio/game-end.mp3")
ten_seconds_sound=pygame.mixer.Sound("C:/Users/nilam/OneDrive/Documents/ameya/python/apps/chess/assets/audio/tenseconds.mp3")

move_piece=pygame.USEREVENT + 1
update_piecePos=pygame.event.Event(move_piece)
bot_input=pygame.USEREVENT + 2
botInput=pygame.event.Event(bot_input)
play=pygame.USEREVENT + 3
pygame.time.set_timer(play, 150)
player_clock=pygame.USEREVENT + 4
pygame.time.set_timer(player_clock, 1000)
draw_clock=pygame.USEREVENT + 5
pygame.time.set_timer(draw_clock, 1000)

undo_move_bt=Button(850, 705, 85, 175, type="img", img=undo_move_img)
restart_bt=Button(850, 497, 85, 175, type="img", img=restart_img)
resign_bt=Button(850, 289, 85, 175, type="img", img=resign_img)
draw_bt=Button(850, 81, 85, 175, type="img", img=white_pawn)

offer_draw_box = ask_draw_box()





game_start_sound.play()
while True :
    for event in pygame.event.get() :
        if event.type==pygame.QUIT :
            pygame.quit()
            sys.exit()

        if not game_end :
            if promotion_active :
                if event.type==pygame.MOUSEBUTTONUP :
                    promotion_active=False
                    if queen_rect.collidepoint(event.pos) :
                        selected_piece.piece='queen'
                    elif rook_rect.collidepoint(event.pos) :
                        selected_piece.piece='rook'
                    elif knight_rect.collidepoint(event.pos) :
                        selected_piece.piece='knight'
                    elif bishop_rect.collidepoint(event.pos) :
                        selected_piece.piece='bishop'
                    else :
                        promotion_active=True
                    selected_piece.update_info()
            else :
                if event.type==pygame.MOUSEBUTTONDOWN :
                    for piece in white_pieces + black_pieces :
                        if piece.piece_rect.collidepoint(event.pos) :
                            selected_piece=piece
                            legal_moves=get_legalMoves(selected_piece,turn)
                            break

                if event.type == pygame.MOUSEBUTTONUP and selected_piece:
                    start_x=selected_piece.x
                    start_y=selected_piece.y
                    start_pos=start_x+(start_y*8)

                    if white=='user' and turn=='white' :
                        gx = int((event.pos[0] - board_x) // cell_size)
                        gy = int((event.pos[1] - board_y) // cell_size)
                        end_pos=gx+(gy*8)

                        gx=max(0, min(7, int(gx)))
                        gy=max(0, min(7, int(gy)))
                    elif black=='user' and turn=='black' :
                        gx = int((event.pos[0] - board_x) // cell_size)
                        gy = int((event.pos[1] - board_y) // cell_size)
                        end_pos=gx+(gy*8)

                        gx=max(0, min(7, int(gx)))
                        gy=max(0, min(7, int(gy)))
                    pygame.event.post(update_piecePos)

                if event.type==play :
                        if bot2_color==turn and not bot_has_moved :
                            pygame.event.post(botInput)
                            bot_has_moved=True
                        elif bot1_color==turn and not bot_has_moved :
                            pygame.event.post(botInput)

                if event.type==bot_input :
                    if white=='bot' and turn=='white' :
                        bot_castling_rights=[None,None,None,None]
                        for piece in white_pieces+black_pieces :
                            if piece.piece=='rook' :
                                if piece.color=='white' :
                                    if piece.start_x==7 :
                                        bot_castling_rights[0]=piece.can_castle
                                    if piece.start_x==0 :
                                        bot_castling_rights[1]=piece.can_castle
                                if piece.color=='black' :
                                    if piece.start_x==7 :
                                        bot_castling_rights[2]=piece.can_castle
                                    if piece.start_x==0 :
                                        bot_castling_rights[3]=piece.can_castle
                        bot_fen=board_to_fen(board, turn, bot_castling_rights, en_passant_sq, moves_since_pm_or_c, total_moves)
                        my_bot.load_board(bot_fen)
                        move=my_bot.select_move()
                        print(move) 
                        if move :
                            selected_piece, start_x, start_y, start_pos, gx, gy, end_pos=get_bot_input(move,white_pieces)
                    elif black=='bot' and turn=='black' :
                        bot_castling_rights=[None,None,None,None]
                        for piece in white_pieces+black_pieces :
                            if piece.piece=='rook' :
                                if piece.color=='white' :
                                    if piece.start_x==7 :
                                        bot_castling_rights[0]=piece.can_castle
                                    if piece.start_x==0 :
                                        bot_castling_rights[1]=piece.can_castle
                                if piece.color=='black' :
                                    if piece.start_x==7 :
                                        bot_castling_rights[2]=piece.can_castle
                                    if piece.start_x==0 :
                                        bot_castling_rights[3]=piece.can_castle
                        bot_fen=board_to_fen(board, turn, bot_castling_rights, en_passant_sq, moves_since_pm_or_c, total_moves)
                        my_bot.load_board(bot_fen)
                        move=my_bot.select_move()
                        print(move)
                        if move :
                            selected_piece, start_x, start_y, start_pos, gx, gy, end_pos=get_bot_input(move,black_pieces)
                    if selected_piece is None:
                        continue
                    legal_moves = get_legalMoves(selected_piece, turn)
                    pygame.event.post(update_piecePos)

                if event.type==player_clock :
                    if turn=='white' :
                        white_time-=1
                    elif turn=='black' :
                        black_time-=1

                if event.type==draw_clock:
                    offer_draw_box.draw_offer_time-=1

                if event.type==move_piece and selected_piece :
                    friendly=white_pieces if selected_piece.color == "white" else black_pieces
                    enemy=white_pieces if selected_piece.color == "black" else black_pieces
                    friendly_occupied=any(p.x == gx and p.y == gy for p in friendly if p != selected_piece)

                    if not friendly_occupied and end_pos in legal_moves:
                        selected_piece.x = gx
                        selected_piece.y = gy
                    else :
                        end_pos=start_x+(start_y*8)

                    castled=False
                    if selected_piece.piece == 'king' and abs(end_pos - start_pos) == 2:
                        if end_pos > start_pos: 
                            rook_start_x = 7
                            rook_end_x = 5
                        else:  
                            rook_start_x = 0
                            rook_end_x = 3

                        for rook in friendly:
                            if rook.piece == 'rook' and rook.x == rook_start_x and rook.y == selected_piece.y:
                                rook.x = rook_end_x
                                board[0 if rook.color=='black' else 7][rook_start_x]='-'
                                board[0 if rook.color=='black' else 7][rook_end_x]=rook
                                rook.update_piece_pixel_pos()
                                rook.can_castle=False
                                castled=True
                                break

                    if selected_piece.piece=='pawn' and abs(selected_piece.start_y-selected_piece.y)==2 and start_pos!=end_pos :
                        en_passant_sq=xy_to_board_num(selected_piece.x, abs(selected_piece.start_y+gy)//2)
                        en_passant_found=0
                    else :
                        if en_passant_found==2 :
                            en_passant_sq=None

                    captured=False
                    if selected_piece.piece=='pawn' and end_pos==en_passant_sq :
                        is_enPassant=True
                        off=1 if selected_piece.color=='white' else -1
                        for piece in enemy :
                            if piece.piece=='pawn' and xy_to_board_num(piece.x,piece.y)==xy_to_board_num(gx,gy) :
                                is_enPassant=False

                        if is_enPassant :
                            for piece in enemy :
                                if piece.piece=='pawn' and piece.x==gx and piece.y==gy+off :
                                    board[gy+off][gx]='-'
                                    enemy.remove(piece)
                                    moves_since_pm_or_c=-1
                                    captured=True
                                    break
                    else :
                        for piece in enemy :
                            if piece.x==selected_piece.x and piece.y==selected_piece.y :
                                enemy.remove(piece)
                                moves_since_pm_or_c=-1
                                captured=True
                                break

                    selected_piece.update_piece_pixel_pos()

                    if start_pos!=end_pos :
                        total_halfmoves+=1
                        en_passant_found+=1
                        moves_since_pm_or_c+=1
                        total_moves=total_halfmoves//2
                        if selected_piece.piece in ['rook','king'] :
                            selected_piece.can_castle=False
                        if selected_piece.piece=='pawn' :
                            moves_since_pm_or_c=0
                        player_num+=1
                        turn=player[player_num%2]
                        board[start_y][start_x]='-'
                        board[gy][gx]=selected_piece
                        white_pieces, black_pieces=board_to_pieces(board)
                        bot_has_moved = False
                        if selected_piece.color=='white' :
                            white_time+=time_increment
                        if selected_piece.color=='black' :
                            black_time+=time_increment
                        for piece in black_pieces+white_pieces :
                            if piece.piece == 'rook' :
                                if piece.color == 'white' :
                                    if piece.start_x == 0 :
                                        w_queen_rook = piece.can_castle
                                    if piece.start_x == 7 :
                                        w_king_rook = piece.can_castle
                                if piece.color == 'black' :
                                    if piece.start_x == 0 :
                                        b_queen_rook = piece.can_castle
                                    if piece.start_x == 7 :
                                        b_king_rook = piece.can_castle

                        positions.append(board_to_fen(board, turn, [w_king_rook, w_queen_rook, b_king_rook, b_queen_rook], en_passant_sq, moves_since_pm_or_c, total_moves))

                    if selected_piece.piece == 'pawn' and selected_piece.y in (0, 7):
                        if (selected_piece.color == 'white' and white == 'user') or (selected_piece.color == 'black' and black == 'user'):
                            promotion_active=True
                        else:
                            selected_piece.piece=my_bot.get_promoted_piece()
                            selected_piece.update_info()
                            promote_sound.play()

                    else:
                        selected_piece = None

                    for y in range(len(board)) :
                        for x in board[y] :
                            code=x.piece_code if x!='-' else '-'
                            print(code,end=' ')
                        print()
                    print()

                    for piece in enemy :
                        if piece.piece=='king' :
                            king_square=piece.get_pos()

                    moved=move_sound
                    if captured :
                        moved=capture_sound
                    if castled :
                        moved=castle_sound
                    if promoted :
                        moved=promote_sound
                    if is_attacked(king_square,turn,white_pieces,black_pieces) :
                        moved=check_sound

                    if start_pos!=end_pos :
                        moved.play()

    p_time=white_time if turn=='white' else black_time
    game_end_state=is_game_end(turn,black_pieces,white_pieces,p_time,is_Bresign,is_Wresign,positions, draw_result)
    if not game_end :
        if game_end_state=='checkmate' :
            game_end_sound.play()
            print('%s won by checkmate' %(player[(player_num+1)%2]))
            game_end=True
        elif game_end_state=='time' :
            print('%s won by time' %(player[(player_num+1)%2]))
            game_end=True
        elif game_end_state=='stalemate' :
            print("Stalemate!")
            game_end=True
        elif game_end_state=='draw' :
            print("It's a draw")
            game_end=True
        elif game_end_state=='w_win' :
            print("Black resigned.\nWhite won!")
            game_end=True
        elif game_end_state=='b_win' :
            print("White resigned.\nBlack won!")
            game_end=True

    screen.fill("#474747")
    draw_board(board_x,board_y)
    for piece in white_pieces + black_pieces:
        piece.draw_piece()
    if selected_piece and not((turn=='white' and white=='bot') or (turn=='black' and black=='bot')) :
        legal_moves=get_legalMoves(selected_piece,turn)
        highlight_legalMoves(legal_moves)
        update_piece_pos(selected_piece)
    w_time_sep=':' if len(str(white_time%60))==2 else ':0'
    b_time_sep=':' if len(str(black_time%60))==2 else ':0'
    drawTitle(84, 25, 895, 200, 50, '#ffffff', '#000000', str(white_time//60)+w_time_sep+str(white_time%60), "center", 0, 4)
    drawTitle(84, 25, 15, 200, 50, '#ffffff', '#000000', str(black_time//60)+b_time_sep+str(black_time%60), "center", 0, 4)
    undo_move_bt.drawButton("#707070", "#616161")
    restart_bt.drawButton("#707070", "#616161")
    resign_bt.drawButton("#707070", "#616161")
    draw_bt.drawButton("#707070", "#616161")

    if promotion_active :
        panel_x=selected_piece.piece_x
        panel_y=selected_piece.piece_y-(cell_size/2) if selected_piece.color=='white' else selected_piece.piece_y-(cell_size*3)-(cell_size/2)
        selection_panel_bg_surf=pygame.Surface((cell_size, cell_size*4))
        selection_panel_bg_surf.fill("#ffffff")
        selection_panel_bg_rect=selection_panel_bg_surf.get_rect(midtop=(panel_x, panel_y))

        queen_x=selected_piece.piece_x
        queen_y=selected_piece.piece_y if selected_piece.color=='white' else selected_piece.piece_y-(cell_size*3)
        queen_surf=white_queen if selected_piece.color=='white' else black_queen
        queen_rect=queen_surf.get_rect(center=(queen_x, queen_y))

        rook_x=selected_piece.piece_x
        rook_y=selected_piece.piece_y+(cell_size) if selected_piece.color=='white' else selected_piece.piece_y-(cell_size*2)
        rook_surf=white_rook if selected_piece.color=='white' else black_rook
        rook_rect=rook_surf.get_rect(center=(rook_x, rook_y))

        knight_x=selected_piece.piece_x
        knight_y=selected_piece.piece_y+(cell_size*2) if selected_piece.color=='white' else selected_piece.piece_y-(cell_size)
        knight_surf=white_knight if selected_piece.color=='white' else black_knight
        knight_rect=knight_surf.get_rect(center=(knight_x, knight_y))

        bishop_x=selected_piece.piece_x
        bishop_y=selected_piece.piece_y+(cell_size*3) if selected_piece.color=='white' else selected_piece.piece_y
        bishop_surf=white_bishop if selected_piece.color=='white' else black_bishop
        bishop_rect=bishop_surf.get_rect(center=(bishop_x, bishop_y))
        
        screen.blit(selection_panel_bg_surf, selection_panel_bg_rect)
        screen.blit(queen_surf, queen_rect)
        screen.blit(rook_surf, rook_rect)
        screen.blit(knight_surf, knight_rect)
        screen.blit(bishop_surf, bishop_rect)
        pygame.display.update()

    if restart_bt.is_clicked() :
        white_time=white_play_time
        black_time=black_play_time
        time_increment=play_time_increment
        is_Wresign=False
        is_Bresign=False
        game_end=False
        positions=["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"]
        white_pieces=[Piece('white','king',4,7),Piece('white','queen',3,7),Piece('white','bishop',2,7),Piece('white','bishop',5,7),Piece('white','knight',1,7),Piece('white','knight',6,7),Piece('white','rook',0,7),Piece('white','rook',7,7),Piece('white','pawn',0,6),Piece('white','pawn',1,6),Piece('white','pawn',2,6),Piece('white','pawn',3,6),Piece('white','pawn',4,6),Piece('white','pawn',5,6),Piece('white','pawn',6,6),Piece('white','pawn',7,6)]
        black_pieces=[Piece('black','king',4,0),Piece('black','queen',3,0),Piece('black','bishop',2,0),Piece('black','bishop',5,0),Piece('black','knight',1,0),Piece('black','knight',6,0),Piece('black','rook',0,0),Piece('black','rook',7,0),Piece('black','pawn',0,1),Piece('black','pawn',1,1),Piece('black','pawn',2,1),Piece('black','pawn',3,1),Piece('black','pawn',4,1),Piece('black','pawn',5,1),Piece('black','pawn',6,1),Piece('black','pawn',7,1)]
        for piece in white_pieces + black_pieces:
            piece.draw_piece()

        board, turn, castling_rights, en_passant_sq, moves_since_pm_or_c, total_moves=fen_to_board(start_fen)

        if turn=='white' :
            player_num=0
        else :
            player_num=1
    
        if castling_rights!=None :
            for piece in black_pieces+white_pieces :
                if piece.piece=='rook' :
                    if piece.start_x==7 and piece.color == "white" :
                        piece.can_castle=castling_rights[0]
                    elif piece.start_x==0 and piece.color == "white" :
                        piece.can_castle=castling_rights[1]
                    elif piece.start_x==7 and piece.color == "black" :
                        piece.can_castle=castling_rights[2]
                    elif piece.start_x==0 and piece.color == "black" :
                        piece.can_castle=castling_rights[3]
                if piece.piece=='king' :
                    piece.can_castle=True
        else :
            for rook in black_pieces+white_pieces :
                if rook.piece in ['rook','king'] :
                    rook.can_castle=False
        promotion_active = False
        draw_asked = False
        draw_result = False
        game_start_sound.play()
    
    if resign_bt.is_clicked() :
        if turn=='black' :
            is_Wresign=True
        else  :
            is_Bresign=True

    if undo_move_bt.is_clicked() and not game_end :
        for _ in range(2) :
            if len(positions) >= 2 :
                board, turn, en_passant_sq, moves_since_pm_or_c, total_moves, player_num, white_pieces, black_pieces = set_board(positions[-2])
                positions.pop(-1)
        for piece in white_pieces + black_pieces :
            piece.update_piece_pixel_pos()

    if draw_bt.is_clicked() and not game_end :
        offer_draw_box.ask_draw(turn)
        draw_asked = True

    if draw_asked:
        offer_draw_box.draw()
        draw_result = offer_draw_box.get_result()
        if draw_result != "in_progress" or offer_draw_box.draw_offer_time <= 0:
            draw_asked = False
        
    pygame.display.update()
    clock.tick(60)
