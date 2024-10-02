#pragma once
#include <fstream>

class Graph {
private:
  std::fstream  _file;
  double  _domainSize;
  int     _center;
  double  _microscopic;

  Graph(const Graph& obj);
  Graph& operator=(const Graph& obj);

public:
  Graph(void);
  ~Graph();
};
