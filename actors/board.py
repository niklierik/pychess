from actors.actor import Actor
from actors.tile import Tile
from actors.texture import TextureActor
import pygame
import typing
import game.color
import game.side
import chess

Color = game.color.PieceColor
Side = game.side.Side


TILESIZE = 64
WIDTH = 8
HEIGHT = 8

promotion = {
    "queen": chess.QUEEN,
    "rook": chess.ROOK,
    "bishop": chess.BISHOP,
    "knight": chess.KNIGHT,
}


class Board(Actor):
    def __init__(self, scene, perspective=Color.WHITE) -> None:
        super().__init__(scene)
        self.chess_board = chess.Board()
        self.tiles: list[Tile] = []
        self._perspective = perspective
        self.chars: list[TextureActor] = []
        self.offset = (50 + TILESIZE, (1080 - TILESIZE * HEIGHT) // 2)
        self.turn_of = Color.WHITE
        if self.game is not None:
            self.rank_textures = self.game.assets.textures.chars.ranks
            self.file_textures = self.game.assets.textures.chars.files
        # for tests
        else:
            self.rank_textures = []
            self.file_textures = []
        self.rank_textures.reverse()
        self.create_tiles()
        self.selected: typing.Union[Tile, None] = None

    @property
    def perspective(self):
        return self._perspective

    @perspective.setter
    def perspective(self, perspective: Color):
        from game.pieces import Piece

        if perspective == self._perspective:
            return

        self.rank_textures.reverse()
        self.file_textures.reverse()
        if self.game is not None:
            self.generate_chars()
        self._perspective = perspective
        pieces: list[typing.Union[None, Piece]] = list([None] * (WIDTH * HEIGHT))
        pieces = list(map(lambda tile: tile.piece, self.tiles))
        pieces.reverse()
        for tile in self.tiles:
            tile.refresh_texture()
            p = pieces[tile.index]
            tile.piece = p
            if p is not None:
                p.tile = tile

    def create_tiles(self):
        self.tiles = [None] * TILESIZE  # type: ignore
        for x in range(0, WIDTH):
            for y in range(0, HEIGHT):
                index = self.index(x, y)
                if index is None:
                    raise Exception("Shouldn't be possible")
                tile = Tile(self.scene, self, index, x, y, self.offset)
                self.tiles[index] = tile  # type: ignore
                tile.init()
        self.add_pieces()
        first: Tile = self.tiles[0]  # type:ignore
        topleft = first.bounds.topleft
        if self.game is not None:
            self.generate_chars()
        self.bounds = pygame.Rect(
            topleft[0] - TILESIZE,
            topleft[1] - TILESIZE,
            TILESIZE * (WIDTH + 2),
            TILESIZE * (HEIGHT + 2),
        )

    def generate_chars(self):
        if self.game is None:
            return
        self.scene.remove_actors(self.chars)
        self.chars.clear()
        for file in range(0, WIDTH):
            self.chars.append(
                TextureActor(
                    self.scene,
                    self.file_textures[file],
                    pygame.Rect(
                        self.offset[0] + TILESIZE // 4 + (file) * TILESIZE,
                        TILESIZE // 4 + self.offset[1] - TILESIZE,
                        TILESIZE // 2,
                        TILESIZE // 2,
                    ),
                )
            )
            self.chars.append(
                TextureActor(
                    self.scene,
                    self.file_textures[file],
                    pygame.Rect(
                        self.offset[0] + TILESIZE // 4 + (file) * TILESIZE,
                        TILESIZE * (HEIGHT + 1)
                        + TILESIZE // 4
                        + self.offset[1]
                        - TILESIZE,
                        TILESIZE // 2,
                        TILESIZE // 2,
                    ),
                )
            )

        for rank in range(0, HEIGHT):
            self.chars.append(
                TextureActor(
                    self.scene,
                    self.rank_textures[rank],
                    pygame.Rect(
                        TILESIZE // 4 + self.offset[0] - TILESIZE,
                        self.offset[1] + TILESIZE // 4 + (rank) * TILESIZE,
                        TILESIZE // 2,
                        TILESIZE // 2,
                    ),
                )
            )
            self.chars.append(
                TextureActor(
                    self.scene,
                    self.rank_textures[rank],
                    pygame.Rect(
                        TILESIZE * (WIDTH + 1)
                        + TILESIZE // 4
                        + self.offset[0]
                        - TILESIZE,
                        self.offset[1] + TILESIZE // 4 + (rank) * TILESIZE,
                        TILESIZE // 2,
                        TILESIZE // 2,
                    ),
                )
            )
        self.scene.actors.extend(self.chars)

    def init(self):
        super().init()

    def add_pieces(self):
        import game.pieces

        pieces: list[game.pieces.Piece] = []
        for color in [Color.WHITE, Color.BLACK]:
            for file in range(0, WIDTH):
                pieces.append(game.pieces.Pawn(self, color, file))
            for side in [Side.QUEEN, Side.KING]:
                pieces.append(game.pieces.Rook(self, color, side))
                pieces.append(game.pieces.Knight(self, color, side))
                pieces.append(game.pieces.Bishop(self, color, side))
            pieces.append(game.pieces.King(self, color))
            pieces.append(game.pieces.Queen(self, color))
        for piece in pieces:
            # registering the pieces to the board
            piece.tile._piece = piece  # type: ignore
            piece.tile.find_legal_moves()  # type: ignore

    def xy(self, index: typing.Union[None, int]):
        if index is None:
            return None
        return (index % WIDTH, index // WIDTH)

    def index(self, x: int, y: int):
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return None
        return x * WIDTH + y

    def from_uci(self, uci: str) -> typing.Union[int, None]:
        if len(uci) != 2:
            raise Exception("Board.from_uci(str) expects the input's length to be 2.")
        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        file = files.index(uci[0])
        rank = int(uci[1])
        return self.index(
            file if self.perspective == Color.WHITE else 8 - file - 1,
            rank - 1 if self.perspective == Color.BLACK else 8 - rank,
        )

    def clear_selection(self):
        for tile in self.tiles:
            tile.selected = False
            tile.can_move_there = False

    def move_from_uci(
        self, uci: str
    ) -> tuple[typing.Union[None, int], typing.Union[None, int]]:
        if len(uci) != 4:
            raise Exception(
                "Board.move_from_uci(str) expects the input's length to be 4."
            )
        return (self.from_uci(uci[:2]), self.from_uci(uci[2:]))

    def find_tile(self, uci: str):
        index = self.from_uci(uci)
        return self.tile(index)

    def find_tiles(self, uci: str):
        return (self.find_tile(uci[:2]), self.find_tile(uci[2:]))

    def tile(self, index: typing.Union[None, int]):
        if index is None:
            return None
        return self.tiles[index]

    def render(self, screen):
        for tile in self.tiles:
            if self.selected is not tile:
                tile.render(screen)
        # render selected last so the selected piece is always visible
        if self.selected is not None:
            self.selected.render(screen)

    def get_moves_from(self, tile_from: Tile):
        moves: list[chess.Move] = []
        for move in self.chess_board.legal_moves:
            move: chess.Move = move
            uci: str = move.uci()
            if uci.startswith(tile_from.__str__()):
                moves.append(move)
        return moves

    def make_move(
        self,
        _from: typing.Union[None, Tile],
        to: typing.Union[None, Tile],
        promoteTo: str = "",
    ):
        if _from is None or to is None:
            return
        # moving
        uci = f"{_from.__str__()}{to.__str__()}{promoteTo}"
        try:
            move: chess.Move = chess.Move.from_uci(uci)
            # if len(promoteTo) > 0:
            #    move.promotion = promotion[promoteTo]
            if not self.chess_board.is_legal(move):
                return
            ### Handle captures
            if self.chess_board.is_capture(move):
                if to.piece is not None:  # may be false if en passant
                    to.piece.tile = None
                if self.chess_board.is_en_passant(move):
                    dir = to.y - _from.y
                    tile = self.tile(self.index(to.x, to.y - dir))
                    assert tile is not None
                    assert tile.piece is not None
                    tile.piece.tile = None

            if _from.piece is not None:
                _from.piece.tile = to
                if move.promotion is not None:
                    assert to.piece is not None
                    assert self.game is not None
                    color = to.piece.color
                    theme = self.game.assets.textures.pieces.regular
                    pieces = theme.white if color == Color.WHITE else theme.black
                    match move.promotion:
                        case chess.KNIGHT:
                            to.piece.original_texture = pieces.knight
                        case chess.BISHOP:
                            to.piece.original_texture = pieces.bishop
                        case chess.ROOK:
                            to.piece.original_texture = pieces.rook
                        case chess.QUEEN:
                            to.piece.original_texture = pieces.queen
                    to.piece.on_resize()

            print(f"{uci} | {self.chess_board.san(move)}")
            _from.selected = False
            to.selected = False
            self.selected = None

            #### Handle Castling
            assert to.piece is not None
            y = 7 if self.perspective == to.piece.color else 0
            from_x = to_x = None
            if self.chess_board.is_kingside_castling(move):
                from_x = 7 if self.perspective == Color.WHITE else 0
                to_x = 5 if self.perspective == Color.WHITE else 2
            if self.chess_board.is_queenside_castling(move):
                from_x = 0 if self.perspective == Color.WHITE else 7
                to_x = 3 if self.perspective == Color.WHITE else 4
            if from_x is not None and to_x is not None:
                _from = self.tile(self.index(from_x, y))
                to = self.tile(self.index(to_x, y))
                assert _from is not None and to is not None
                assert _from.piece is not None
                _from.piece.tile = to

            ### Clean up
            self.chess_board.push(move)
            for tile in self.tiles:
                tile.can_move_there = False
                tile.selected = False
                tile.marked = False
                tile.find_legal_moves()
        except ValueError or chess.IllegalMoveError or chess.InvalidMoveError as e:
            print(e)
        self.turn_of = self.turn_of.opposite()
        return

    def update(self, delta):
        for tile in self.tiles:
            tile.update(delta)

    def on_mouse_button_up(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        super().on_mouse_button_up(event, pos, button)
        for tile in self.tiles:
            if tile.render_bounds.collidepoint(pos):
                tile.on_mouse_button_up(event, pos, button)

    def on_window_resize(self, event: pygame.event.Event):
        for tile in self.tiles:
            tile.on_window_resize(event)

    def dispose(self):
        for tile in self.tiles:
            tile.dispose()
