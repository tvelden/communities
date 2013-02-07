# Various flags

CXX  = g++
LINK = $(CXX)
#CXXFLAGS = -I -Wall -g 
CXXFLAGS = -I -Wall -O3 -funroll-loops -pipe
LFLAGS = -lm


TARGET  = conf-infomap

HEADER  = conf-infomap.h GreedyBase.h Greedy.h Node.h
FILES = conf-infomap.cc GreedyBase.cc Greedy.cc Node.cc mersenne.cpp stoc1.cpp userintf.cpp

OBJECTS = $(FILES:.cc=.o)

$(TARGET): ${OBJECTS}
	$(LINK) $^ $(LFLAGS) -o $@

all: $(TARGET)

clean:
	rm -f $(OBJECTS)

distclean:
	rm -f $(OBJECTS) $(TARGET)

# Compile and dependency
$(OBJECTS): $(HEADER) Makefile




