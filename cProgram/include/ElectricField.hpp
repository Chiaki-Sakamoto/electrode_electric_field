#pragma once

#include <cstdlib>
#include <vector>

class ElectricField {
private:
  double  _Ex;
  double  _Ey;
  double  _epsilonZero;
  double  _conv;
  std::vector<double> _phi;
  std::vector<double> _rho;
  double  _maxPhi;
  double  _maxErr;
  double  _curErr;
  double  _prevPhi;

  ElectricField(const ElectricField& obj);
  ElectricField& operator=(const ElectricField& obj);

public:
  ElectricField(void);
  ~ElectricField();
};
