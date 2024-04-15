SRC_DIR := src
OBJ_DIR := obj
BIN_DIR := bin

EXE := $(BIN_DIR)/deejay
SRC := $(wildcard $(SRC_DIR)/*.c)
OBJ := $(SRC:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# Dependencies
MHTTPD_LIB := -lmicrohttpd
LIBXML_INC := -I/usr/include/libxml2
LIBXML_LIB := -lxml2
GLIB_INC := -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include
GLIB_LIB := -lglib-2.0

CC := gcc
CPPFLAGS := -Iinclude $(LIBXML_INC) $(GLIB_INC) -MMD -MP
CFLAGS := -Wall -Werror
LDLIBS := $(MHTTPD_LIB) $(LIBXML_LIB) $(GLIB_LIB)

all: $(EXE)

.PHONY: all clean

$(EXE): $(OBJ) | $(BIN_DIR)
	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BIN_DIR) $(OBJ_DIR):
	mkdir -p $@

clean:
	@ $(RM) -rv $(BIN_DIR) $(OBJ_DIR)

-include $(OBJ:.o=.d)
