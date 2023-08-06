
/*
 * block2: Efficient MPO implementation of quantum chemistry DMRG
 * Copyright (C) 2020 Huanchen Zhai <hczhai@caltech.edu>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 *
 */

#pragma once

#include "../block2.hpp"
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>

namespace py = pybind11;
using namespace block2;

PYBIND11_MAKE_OPAQUE(vector<int>);
PYBIND11_MAKE_OPAQUE(vector<char>);
PYBIND11_MAKE_OPAQUE(vector<long long int>);
PYBIND11_MAKE_OPAQUE(vector<uint8_t>);
PYBIND11_MAKE_OPAQUE(vector<uint16_t>);
PYBIND11_MAKE_OPAQUE(vector<uint32_t>);
PYBIND11_MAKE_OPAQUE(vector<double>);
PYBIND11_MAKE_OPAQUE(vector<complex<double>>);
PYBIND11_MAKE_OPAQUE(vector<size_t>);
PYBIND11_MAKE_OPAQUE(vector<vector<uint32_t>>);
PYBIND11_MAKE_OPAQUE(vector<vector<double>>);
PYBIND11_MAKE_OPAQUE(vector<vector<vector<double>>>);
PYBIND11_MAKE_OPAQUE(vector<vector<int>>);
PYBIND11_MAKE_OPAQUE(vector<pair<int, int>>);
PYBIND11_MAKE_OPAQUE(vector<pair<long long int, int>>);
PYBIND11_MAKE_OPAQUE(vector<ActiveTypes>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<Tensor>>);
PYBIND11_MAKE_OPAQUE(vector<vector<shared_ptr<Tensor>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<CSRMatrixRef>>);
// SZ
PYBIND11_MAKE_OPAQUE(vector<vector<vector<pair<SZ, double>>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<OpExpr<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<OpProduct<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<OpElement<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<StateInfo<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<pair<shared_ptr<OpExpr<SZ>>, double>>);
PYBIND11_MAKE_OPAQUE(vector<pair<SZ, shared_ptr<SparseMatrixInfo<SZ>>>>);
PYBIND11_MAKE_OPAQUE(
    vector<vector<pair<SZ, shared_ptr<SparseMatrixInfo<SZ>>>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<SparseMatrixInfo<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<SparseMatrix<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<OperatorTensor<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<Symbolic<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<SymbolicRowVector<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<SymbolicColumnVector<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<SymbolicMatrix<SZ>>>);
PYBIND11_MAKE_OPAQUE(map<OpNames, shared_ptr<SparseMatrix<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<map<OpNames, shared_ptr<SparseMatrix<SZ>>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<Partition<SZ>>>);
PYBIND11_MAKE_OPAQUE(map<shared_ptr<OpExpr<SZ>>, shared_ptr<SparseMatrix<SZ>>,
                         op_expr_less<SZ>>);
PYBIND11_MAKE_OPAQUE(vector<pair<pair<SZ, SZ>, shared_ptr<Tensor>>>);
PYBIND11_MAKE_OPAQUE(vector<vector<pair<pair<SZ, SZ>, shared_ptr<Tensor>>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<MPS<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<MovingEnvironment<SZ>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<EffectiveHamiltonian<SZ>>>);
// SU2
PYBIND11_MAKE_OPAQUE(vector<vector<vector<pair<SU2, double>>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<OpExpr<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<OpProduct<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<OpElement<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<StateInfo<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<pair<shared_ptr<OpExpr<SU2>>, double>>);
PYBIND11_MAKE_OPAQUE(vector<pair<SU2, shared_ptr<SparseMatrixInfo<SU2>>>>);
PYBIND11_MAKE_OPAQUE(
    vector<vector<pair<SU2, shared_ptr<SparseMatrixInfo<SU2>>>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<SparseMatrixInfo<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<SparseMatrix<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<OperatorTensor<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<Symbolic<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<SymbolicRowVector<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<SymbolicColumnVector<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<SymbolicMatrix<SU2>>>);
PYBIND11_MAKE_OPAQUE(map<OpNames, shared_ptr<SparseMatrix<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<map<OpNames, shared_ptr<SparseMatrix<SU2>>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<Partition<SU2>>>);
PYBIND11_MAKE_OPAQUE(map<shared_ptr<OpExpr<SU2>>, shared_ptr<SparseMatrix<SU2>>,
                         op_expr_less<SU2>>);
PYBIND11_MAKE_OPAQUE(vector<pair<pair<SU2, SU2>, shared_ptr<Tensor>>>);
PYBIND11_MAKE_OPAQUE(vector<vector<pair<pair<SU2, SU2>, shared_ptr<Tensor>>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<MPS<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<MovingEnvironment<SU2>>>);
PYBIND11_MAKE_OPAQUE(vector<shared_ptr<EffectiveHamiltonian<SU2>>>);
PYBIND11_MAKE_OPAQUE(map<string, string>);

template <typename T> struct Array {
    T *data;
    size_t n;
    Array(T *data, size_t n) : data(data), n(n) {}
    T &operator[](size_t idx) { return data[idx]; }
};

template <typename T, typename... Args>
size_t printable(const T &p, const Args &...) {
    return (size_t)&p;
}

template <typename T>
auto printable(const T &p)
    -> decltype(declval<ostream &>() << declval<T>(), T()) {
    return p;
}

template <typename T>
py::class_<Array<T>, shared_ptr<Array<T>>> bind_array(py::module &m,
                                                      const char *name) {
    return py::class_<Array<T>, shared_ptr<Array<T>>>(m, name)
        .def(
            "__setitem__",
            [](Array<T> *self, size_t i, const T &t) {
                self->operator[](i) = t;
            },
            py::keep_alive<1, 3>())
        .def("__getitem__",
             [](Array<T> *self, size_t i) { return self->operator[](i); })
        .def("__len__", [](Array<T> *self) { return self->n; })
        .def("__repr__",
             [name](Array<T> *self) {
                 stringstream ss;
                 ss << name << "(LEN=" << self->n << ")[";
                 for (size_t i = 0; i < self->n; i++)
                     ss << printable<T>(self->data[i]) << ",";
                 ss << "]";
                 return ss.str();
             })
        .def(
            "__iter__",
            [](Array<T> *self) {
                return py::make_iterator<
                    py::return_value_policy::reference_internal, T *, T *, T &>(
                    self->data, self->data + self->n);
            },
            py::keep_alive<0, 1>());
}

template <typename S>
auto bind_cg(py::module &m) -> decltype(typename S::is_sz_t()) {
    py::class_<CG<S>, shared_ptr<CG<S>>>(m, "CG")
        .def(py::init<>())
        .def(py::init<int>())
        .def("initialize", [](CG<S> *self) { self->initialize(); })
        .def("deallocate", &CG<S>::deallocate)
        .def("wigner_6j", &CG<S>::wigner_6j, py::arg("tja"), py::arg("tjb"),
             py::arg("tjc"), py::arg("tjd"), py::arg("tje"), py::arg("tjf"))
        .def("wigner_9j", &CG<S>::wigner_9j, py::arg("tja"), py::arg("tjb"),
             py::arg("tjc"), py::arg("tjd"), py::arg("tje"), py::arg("tjf"),
             py::arg("tjg"), py::arg("tjh"), py::arg("tji"))
        .def("racah", &CG<S>::racah, py::arg("ta"), py::arg("tb"),
             py::arg("tc"), py::arg("td"), py::arg("te"), py::arg("tf"))
        .def("transpose_cg", &CG<S>::transpose_cg, py::arg("td"), py::arg("tl"),
             py::arg("tr"));
}

template <typename S>
auto bind_cg(py::module &m) -> decltype(typename S::is_su2_t()) {
    py::class_<CG<S>, shared_ptr<CG<S>>>(m, "CG")
        .def(py::init<>())
        .def(py::init<int>())
        .def("initialize", [](CG<S> *self) { self->initialize(); })
        .def("deallocate", &CG<S>::deallocate)
        .def_static("triangle", &CG<S>::triangle, py::arg("tja"),
                    py::arg("tjb"), py::arg("tjc"))
        .def("sqrt_delta", &CG<S>::sqrt_delta, py::arg("tja"), py::arg("tjb"),
             py::arg("tjc"))
        .def("cg", &CG<S>::cg, py::arg("tja"), py::arg("tjb"), py::arg("tjc"),
             py::arg("tma"), py::arg("tmb"), py::arg("tmc"))
        .def("wigner_3j", &CG<S>::wigner_3j, py::arg("tja"), py::arg("tjb"),
             py::arg("tjc"), py::arg("tma"), py::arg("tmb"), py::arg("tmc"))
        .def("wigner_6j", &CG<S>::wigner_6j, py::arg("tja"), py::arg("tjb"),
             py::arg("tjc"), py::arg("tjd"), py::arg("tje"), py::arg("tjf"))
        .def("wigner_9j", &CG<S>::wigner_9j, py::arg("tja"), py::arg("tjb"),
             py::arg("tjc"), py::arg("tjd"), py::arg("tje"), py::arg("tjf"),
             py::arg("tjg"), py::arg("tjh"), py::arg("tji"))
        .def("racah", &CG<S>::racah, py::arg("ta"), py::arg("tb"),
             py::arg("tc"), py::arg("td"), py::arg("te"), py::arg("tf"))
        .def("transpose_cg", &CG<S>::transpose_cg, py::arg("td"), py::arg("tl"),
             py::arg("tr"));
}

template <typename S>
auto bind_spin_specific(py::module &m) -> decltype(typename S::is_su2_t()) {

    py::class_<PDM2MPOQC<S>, shared_ptr<PDM2MPOQC<S>>, MPO<S>>(m, "PDM2MPOQC")
        .def(py::init<const Hamiltonian<S> &>(), py::arg("hamil"))
        .def("get_matrix", &PDM2MPOQC<S>::template get_matrix<double>)
        .def("get_matrix", &PDM2MPOQC<S>::template get_matrix<complex<double>>)
        .def("get_matrix_spatial",
             &PDM2MPOQC<S>::template get_matrix_spatial<double>)
        .def("get_matrix_spatial",
             &PDM2MPOQC<S>::template get_matrix_spatial<complex<double>>);
}

template <typename S>
auto bind_spin_specific(py::module &m) -> decltype(typename S::is_sz_t()) {

    py::class_<PDM2MPOQC<S>, shared_ptr<PDM2MPOQC<S>>, MPO<S>>(m, "PDM2MPOQC")
        .def_property_readonly_static(
            "s_all", [](py::object) { return PDM2MPOQC<S>::s_all; })
        .def_property_readonly_static(
            "s_minimal", [](py::object) { return PDM2MPOQC<S>::s_minimal; })
        .def(py::init<const Hamiltonian<S> &>(), py::arg("hamil"))
        .def(py::init<const Hamiltonian<S> &, uint16_t>(), py::arg("hamil"),
             py::arg("mask"))
        .def("get_matrix", &PDM2MPOQC<S>::template get_matrix<double>)
        .def("get_matrix", &PDM2MPOQC<S>::template get_matrix<complex<double>>)
        .def("get_matrix_spatial",
             &PDM2MPOQC<S>::template get_matrix_spatial<double>)
        .def("get_matrix_spatial",
             &PDM2MPOQC<S>::template get_matrix_spatial<complex<double>>);

    py::class_<SumMPOQC<S>, shared_ptr<SumMPOQC<S>>, MPO<S>>(m, "SumMPOQC")
        .def_readwrite("ts", &SumMPOQC<S>::ts)
        .def(py::init<const HamiltonianQC<S> &, const vector<uint16_t> &>(),
             py::arg("hamil"), py::arg("pts"));
}

template <typename S> void bind_expr(py::module &m) {
    py::class_<OpExpr<S>, shared_ptr<OpExpr<S>>>(m, "OpExpr")
        .def(py::init<>())
        .def("get_type", &OpExpr<S>::get_type)
        .def(py::self == py::self)
        .def("__repr__", &to_str<S>);

    py::bind_vector<vector<pair<shared_ptr<OpExpr<S>>, double>>>(
        m, "VectorPExprDouble");

    py::class_<OpElement<S>, shared_ptr<OpElement<S>>, OpExpr<S>>(m,
                                                                  "OpElement")
        .def(py::init<OpNames, SiteIndex, S>())
        .def(py::init<OpNames, SiteIndex, S, double>())
        .def_readwrite("name", &OpElement<S>::name)
        .def_readwrite("site_index", &OpElement<S>::site_index)
        .def_readwrite("factor", &OpElement<S>::factor)
        .def_readwrite("q_label", &OpElement<S>::q_label)
        .def("abs", &OpElement<S>::abs)
        .def("__mul__", &OpElement<S>::operator*)
        .def(py::self == py::self)
        .def(py::self < py::self)
        .def("__hash__", &OpElement<S>::hash);

    py::class_<OpElementRef<S>, shared_ptr<OpElementRef<S>>, OpExpr<S>>(
        m, "OpElementRef")
        .def(py::init<const shared_ptr<OpElement<S>> &, int8_t, int8_t>())
        .def_readwrite("op", &OpElementRef<S>::op)
        .def_readwrite("factor", &OpElementRef<S>::factor)
        .def_readwrite("trans", &OpElementRef<S>::trans);

    py::class_<OpProduct<S>, shared_ptr<OpProduct<S>>, OpExpr<S>>(m,
                                                                  "OpProduct")
        .def(py::init<const shared_ptr<OpElement<S>> &, double>())
        .def(py::init<const shared_ptr<OpElement<S>> &, double, uint8_t>())
        .def(py::init<const shared_ptr<OpElement<S>> &,
                      const shared_ptr<OpElement<S>> &, double>())
        .def(py::init<const shared_ptr<OpElement<S>> &,
                      const shared_ptr<OpElement<S>> &, double, uint8_t>())
        .def_readwrite("factor", &OpProduct<S>::factor)
        .def_readwrite("conj", &OpProduct<S>::conj)
        .def_readwrite("a", &OpProduct<S>::a)
        .def_readwrite("b", &OpProduct<S>::b)
        .def("__hash__", &OpProduct<S>::hash);

    py::class_<OpSumProd<S>, shared_ptr<OpSumProd<S>>, OpProduct<S>>(
        m, "OpSumProd")
        .def(py::init<const shared_ptr<OpElement<S>> &,
                      const vector<shared_ptr<OpElement<S>>> &,
                      const vector<bool> &, double, uint8_t,
                      const shared_ptr<OpElement<S>> &>())
        .def(py::init<const shared_ptr<OpElement<S>> &,
                      const vector<shared_ptr<OpElement<S>>> &,
                      const vector<bool> &, double, uint8_t>())
        .def(py::init<const shared_ptr<OpElement<S>> &,
                      const vector<shared_ptr<OpElement<S>>> &,
                      const vector<bool> &, double>())
        .def(py::init<const vector<shared_ptr<OpElement<S>>> &,
                      const shared_ptr<OpElement<S>> &, const vector<bool> &,
                      double, uint8_t, const shared_ptr<OpElement<S>> &>())
        .def(py::init<const vector<shared_ptr<OpElement<S>>> &,
                      const shared_ptr<OpElement<S>> &, const vector<bool> &,
                      double, uint8_t>())
        .def(py::init<const vector<shared_ptr<OpElement<S>>> &,
                      const shared_ptr<OpElement<S>> &, const vector<bool> &,
                      double>())
        .def_readwrite("ops", &OpSumProd<S>::ops)
        .def_readwrite("conjs", &OpSumProd<S>::conjs)
        .def_readwrite("c", &OpSumProd<S>::c);

    py::class_<OpSum<S>, shared_ptr<OpSum<S>>, OpExpr<S>>(m, "OpSum")
        .def(py::init<const vector<shared_ptr<OpProduct<S>>> &>())
        .def_readwrite("strings", &OpSum<S>::strings);

    py::bind_vector<vector<shared_ptr<OpExpr<S>>>>(m, "VectorOpExpr");
    py::bind_vector<vector<shared_ptr<OpElement<S>>>>(m, "VectorOpElement");
    py::bind_vector<vector<shared_ptr<OpProduct<S>>>>(m, "VectorOpProduct");

    struct PySymbolic : Symbolic<S> {
        using Symbolic<S>::Symbolic;
        SymTypes get_type() const override {
            PYBIND11_OVERLOAD_PURE(const SymTypes, Symbolic<S>, get_type, );
        }
        shared_ptr<Symbolic<S>> copy() const override {
            PYBIND11_OVERLOAD_PURE(shared_ptr<Symbolic<S>>, Symbolic<S>,
                                   copy, );
        }
    };

    py::class_<Symbolic<S>, PySymbolic, shared_ptr<Symbolic<S>>>(m, "Symbolic")
        .def(py::init<int, int>())
        .def_readwrite("m", &Symbolic<S>::m)
        .def_readwrite("n", &Symbolic<S>::n)
        .def_readwrite("data", &Symbolic<S>::data)
        .def("get_type", [](Symbolic<S> *self) { return self->get_type(); })
        .def("__matmul__",
             [](const shared_ptr<Symbolic<S>> &self,
                const shared_ptr<Symbolic<S>> &other) { return self * other; });

    py::class_<SymbolicRowVector<S>, shared_ptr<SymbolicRowVector<S>>,
               Symbolic<S>>(m, "SymbolicRowVector")
        .def(py::init<int>())
        .def("__getitem__",
             [](SymbolicRowVector<S> *self, int idx) { return (*self)[idx]; })
        .def("__setitem__",
             [](SymbolicRowVector<S> *self, int idx,
                const shared_ptr<OpExpr<S>> &v) { (*self)[idx] = v; })
        .def("__len__", [](SymbolicRowVector<S> *self) { return self->n; })
        .def("copy", &SymbolicRowVector<S>::copy);

    py::class_<SymbolicColumnVector<S>, shared_ptr<SymbolicColumnVector<S>>,
               Symbolic<S>>(m, "SymbolicColumnVector")
        .def(py::init<int>())
        .def("__getitem__", [](SymbolicColumnVector<S> *self,
                               int idx) { return (*self)[idx]; })
        .def("__setitem__",
             [](SymbolicColumnVector<S> *self, int idx,
                const shared_ptr<OpExpr<S>> &v) { (*self)[idx] = v; })
        .def("__len__", [](SymbolicColumnVector<S> *self) { return self->m; })
        .def("copy", &SymbolicColumnVector<S>::copy);

    py::class_<SymbolicMatrix<S>, shared_ptr<SymbolicMatrix<S>>, Symbolic<S>>(
        m, "SymbolicMatrix")
        .def(py::init<int, int>())
        .def_readwrite("indices", &SymbolicMatrix<S>::indices)
        .def("__setitem__",
             [](SymbolicMatrix<S> *self, int i, int j,
                const shared_ptr<OpExpr<S>> &v) {
                 (*self)[{i, j}] = v;
             })
        .def("copy", &SymbolicMatrix<S>::copy);

    py::bind_vector<vector<shared_ptr<Symbolic<S>>>>(m, "VectorSymbolic");
    py::bind_vector<vector<shared_ptr<SymbolicRowVector<S>>>>(
        m, "VectorSymbolicRowVector");
    py::bind_vector<vector<shared_ptr<SymbolicColumnVector<S>>>>(
        m, "VectorSymbolicColumnVector");
    py::bind_vector<vector<shared_ptr<SymbolicMatrix<S>>>>(
        m, "VectorSymbolicMatrix");
}

template <typename S> void bind_state_info(py::module &m, const string &name) {

    bind_array<StateInfo<S>>(m, "ArrayStateInfo");
    bind_array<S>(m, ("Array" + name).c_str());
    bind_array<vector<pair<S, shared_ptr<SparseMatrixInfo<S>>>>>(
        m, "ArrayVectorPLMatInfo");
    py::bind_vector<vector<shared_ptr<StateInfo<S>>>>(m, "VectorStateInfo");
    py::bind_vector<vector<pair<S, double>>>(m, "VectorPSDouble");
    py::bind_vector<vector<vector<pair<S, double>>>>(m, "VectorVectorPSDouble");
    py::bind_vector<vector<vector<vector<pair<S, double>>>>>(
        m, "VectorVectorVectorPSDouble");

    py::class_<StateInfo<S>, shared_ptr<StateInfo<S>>>(m, "StateInfo")
        .def(py::init<>())
        .def(py::init<S>())
        .def_readwrite("n", &StateInfo<S>::n)
        .def_readwrite("n_states_total", &StateInfo<S>::n_states_total)
        .def_property_readonly(
            "quanta",
            [](StateInfo<S> *self) { return Array<S>(self->quanta, self->n); })
        .def_property_readonly("n_states",
                               [](StateInfo<S> *self) {
                                   return Array<ubond_t>(self->n_states,
                                                         self->n);
                               })
        .def("load_data",
             (void (StateInfo<S>::*)(const string &)) & StateInfo<S>::load_data)
        .def("save_data", (void (StateInfo<S>::*)(const string &) const) &
                              StateInfo<S>::save_data)
        .def("allocate",
             [](StateInfo<S> *self, int length) { self->allocate(length); })
        .def("deallocate", &StateInfo<S>::deallocate)
        .def("reallocate", &StateInfo<S>::reallocate, py::arg("length"))
        .def("sort_states", &StateInfo<S>::sort_states)
        .def("copy_data_to", &StateInfo<S>::copy_data_to)
        .def("deep_copy", &StateInfo<S>::deep_copy)
        .def("collect", &StateInfo<S>::collect,
             py::arg("target") = S(S::invalid))
        .def("find_state", &StateInfo<S>::find_state)
        .def_static("tensor_product_ref",
                    (StateInfo<S>(*)(const StateInfo<S> &, const StateInfo<S> &,
                                     const StateInfo<S> &)) &
                        StateInfo<S>::tensor_product)
        .def_static(
            "tensor_product",
            (StateInfo<S>(*)(const StateInfo<S> &, const StateInfo<S> &, S)) &
                StateInfo<S>::tensor_product)
        .def_static("get_connection_info", &StateInfo<S>::get_connection_info)
        .def_static("filter", &StateInfo<S>::filter)
        .def("__repr__", [](StateInfo<S> *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });
}

template <typename S> void bind_sparse(py::module &m) {

    py::class_<typename SparseMatrixInfo<S>::ConnectionInfo,
               shared_ptr<typename SparseMatrixInfo<S>::ConnectionInfo>>(
        m, "ConnectionInfo")
        .def(py::init<>())
        .def_property_readonly(
            "n",
            [](typename SparseMatrixInfo<S>::ConnectionInfo *self) {
                return self->n[4];
            })
        .def_readwrite("nc", &SparseMatrixInfo<S>::ConnectionInfo::nc)
        .def("deallocate", &SparseMatrixInfo<S>::ConnectionInfo::deallocate)
        .def("__repr__",
             [](typename SparseMatrixInfo<S>::ConnectionInfo *self) {
                 stringstream ss;
                 ss << *self;
                 return ss.str();
             });

    py::class_<SparseMatrixInfo<S>, shared_ptr<SparseMatrixInfo<S>>>(
        m, "SparseMatrixInfo")
        .def(py::init<>())
        .def_readwrite("delta_quantum", &SparseMatrixInfo<S>::delta_quantum)
        .def_readwrite("is_fermion", &SparseMatrixInfo<S>::is_fermion)
        .def_readwrite("is_wavefunction", &SparseMatrixInfo<S>::is_wavefunction)
        .def_readwrite("n", &SparseMatrixInfo<S>::n)
        .def_readwrite("cinfo", &SparseMatrixInfo<S>::cinfo)
        .def_property_readonly("quanta",
                               [](SparseMatrixInfo<S> *self) {
                                   return Array<S>(self->quanta, self->n);
                               })
        .def_property_readonly("n_states_total",
                               [](SparseMatrixInfo<S> *self) {
                                   return py::array_t<uint32_t>(
                                       self->n, self->n_states_total);
                               })
        .def_property_readonly("n_states_bra",
                               [](SparseMatrixInfo<S> *self) {
                                   return py::array_t<ubond_t>(
                                       self->n, self->n_states_bra);
                               })
        .def_property_readonly("n_states_ket",
                               [](SparseMatrixInfo<S> *self) {
                                   return py::array_t<ubond_t>(
                                       self->n, self->n_states_ket);
                               })
        .def("initialize", &SparseMatrixInfo<S>::initialize, py::arg("bra"),
             py::arg("ket"), py::arg("dq"), py::arg("is_fermion"),
             py::arg("wfn") = false)
        .def("initialize_trans_contract",
             &SparseMatrixInfo<S>::initialize_trans_contract)
        .def("initialize_contract", &SparseMatrixInfo<S>::initialize_contract)
        .def("initialize_dm", &SparseMatrixInfo<S>::initialize_dm)
        .def("find_state", &SparseMatrixInfo<S>::find_state, py::arg("q"),
             py::arg("start") = 0)
        .def_property_readonly("total_memory",
                               &SparseMatrixInfo<S>::get_total_memory)
        .def("allocate", &SparseMatrixInfo<S>::allocate, py::arg("length"),
             py::arg("ptr") = nullptr)
        .def("extract_state_info", &SparseMatrixInfo<S>::extract_state_info,
             py::arg("right"))
        .def("deallocate", &SparseMatrixInfo<S>::deallocate)
        .def("reallocate", &SparseMatrixInfo<S>::reallocate, py::arg("length"))
        .def("__repr__", [](SparseMatrixInfo<S> *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });

    py::class_<SparseMatrix<S>, shared_ptr<SparseMatrix<S>>>(m, "SparseMatrix")
        .def(py::init<>())
        .def_readwrite("info", &SparseMatrix<S>::info)
        .def_readwrite("factor", &SparseMatrix<S>::factor)
        .def_readwrite("total_memory", &SparseMatrix<S>::total_memory)
        .def("get_type", &SparseMatrix<S>::get_type)
        .def_property(
            "data",
            [](SparseMatrix<S> *self) {
                return py::array_t<double>(self->total_memory, self->data);
            },
            [](SparseMatrix<S> *self, const py::array_t<double> &v) {
                assert(v.size() == self->total_memory);
                memcpy(self->data, v.data(),
                       sizeof(double) * self->total_memory);
            })
        .def("clear", &SparseMatrix<S>::clear)
        .def("load_data",
             (void (SparseMatrix<S>::*)(
                 const string &, bool,
                 const shared_ptr<Allocator<uint32_t>> &)) &
                 SparseMatrix<S>::load_data,
             py::arg("filename"), py::arg("load_info") = false,
             py::arg("i_alloc") = nullptr)
        .def("save_data",
             (void (SparseMatrix<S>::*)(const string &, bool) const) &
                 SparseMatrix<S>::save_data,
             py::arg("filename"), py::arg("save_info") = false)
        .def("copy_data_from", &SparseMatrix<S>::copy_data_from)
        .def("selective_copy_from", &SparseMatrix<S>::selective_copy_from)
        .def("sparsity", &SparseMatrix<S>::sparsity)
        .def("allocate",
             [](SparseMatrix<S> *self,
                const shared_ptr<SparseMatrixInfo<S>> &info) {
                 self->allocate(info);
             })
        .def("deallocate", &SparseMatrix<S>::deallocate)
        .def("reallocate",
             (void (SparseMatrix<S>::*)(size_t)) & SparseMatrix<S>::reallocate,
             py::arg("length"))
        .def("trace", &SparseMatrix<S>::trace)
        .def("norm", &SparseMatrix<S>::norm)
        .def("__getitem__",
             [](SparseMatrix<S> *self, int idx) { return (*self)[idx]; })
        .def("__setitem__",
             [](SparseMatrix<S> *self, int idx, const py::array_t<double> &v) {
                 assert(v.size() == (*self)[idx].size());
                 memcpy((*self)[idx].data, v.data(), sizeof(double) * v.size());
             })
        .def("left_split",
             [](SparseMatrix<S> *self, ubond_t bond_dim) {
                 shared_ptr<SparseMatrix<S>> left, right;
                 self->left_split(left, right, bond_dim);
                 return make_tuple(left, right);
             })
        .def("right_split",
             [](SparseMatrix<S> *self, ubond_t bond_dim) {
                 shared_ptr<SparseMatrix<S>> left, right;
                 self->right_split(left, right, bond_dim);
                 return make_tuple(left, right);
             })
        .def("pseudo_inverse", &SparseMatrix<S>::pseudo_inverse,
             py::arg("bond_dim"), py::arg("svd_eps") = 1E-4,
             py::arg("svd_cutoff") = 1E-12)
        .def("left_svd",
             [](SparseMatrix<S> *self) {
                 vector<S> qs;
                 vector<shared_ptr<Tensor>> l, s, r;
                 self->left_svd(qs, l, s, r);
                 return make_tuple(qs, l, s, r);
             })
        .def("right_svd",
             [](SparseMatrix<S> *self) {
                 vector<S> qs;
                 vector<shared_ptr<Tensor>> l, s, r;
                 self->right_svd(qs, l, s, r);
                 return make_tuple(qs, l, s, r);
             })
        .def("left_canonicalize", &SparseMatrix<S>::left_canonicalize,
             py::arg("rmat"))
        .def("right_canonicalize", &SparseMatrix<S>::right_canonicalize,
             py::arg("lmat"))
        .def("left_multiply", &SparseMatrix<S>::left_multiply, py::arg("lmat"),
             py::arg("l"), py::arg("m"), py::arg("r"), py::arg("lm"),
             py::arg("lm_cinfo"))
        .def("right_multiply", &SparseMatrix<S>::right_multiply,
             py::arg("rmat"), py::arg("l"), py::arg("m"), py::arg("r"),
             py::arg("mr"), py::arg("mr_cinfo"))
        .def("randomize", &SparseMatrix<S>::randomize, py::arg("a") = 0.0,
             py::arg("b") = 1.0)
        .def("normalize", &SparseMatrix<S>::normalize)
        .def("contract", &SparseMatrix<S>::contract, py::arg("lmat"),
             py::arg("rmat"), py::arg("trace_right") = false)
        .def("swap_to_fused_left", &SparseMatrix<S>::swap_to_fused_left)
        .def("swap_to_fused_right", &SparseMatrix<S>::swap_to_fused_right)
        .def("__repr__", [](SparseMatrix<S> *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });

    py::class_<CSRSparseMatrix<S>, shared_ptr<CSRSparseMatrix<S>>,
               SparseMatrix<S>>(m, "CSRSparseMatrix")
        .def(py::init<>())
        .def_readwrite("csr_data", &CSRSparseMatrix<S>::csr_data)
        .def("__getitem__",
             [](CSRSparseMatrix<S> *self, int idx) { return (*self)[idx]; })
        .def("__setitem__",
             [](CSRSparseMatrix<S> *self, int idx, const CSRMatrixRef &v) {
                 (*self)[idx].deallocate();
                 (*self)[idx] = v;
             })
        .def("from_dense", &CSRSparseMatrix<S>::from_dense)
        .def("wrap_dense", &CSRSparseMatrix<S>::wrap_dense)
        .def("to_dense", &CSRSparseMatrix<S>::to_dense);

    py::class_<ArchivedSparseMatrix<S>, shared_ptr<ArchivedSparseMatrix<S>>,
               SparseMatrix<S>>(m, "ArchivedSparseMatrix")
        .def(py::init<const string &, int64_t>())
        .def_readwrite("filename", &ArchivedSparseMatrix<S>::filename)
        .def_readwrite("offset", &ArchivedSparseMatrix<S>::offset)
        .def("load_archive", &ArchivedSparseMatrix<S>::load_archive)
        .def("save_archive", &ArchivedSparseMatrix<S>::save_archive);

    py::class_<DelayedSparseMatrix<S>, shared_ptr<DelayedSparseMatrix<S>>,
               SparseMatrix<S>>(m, "DelayedSparseMatrix")
        .def(py::init<>())
        .def("build", &DelayedSparseMatrix<S>::build)
        .def("copy", &DelayedSparseMatrix<S>::copy)
        .def("selective_copy", &DelayedSparseMatrix<S>::selective_copy);

    py::class_<DelayedSparseMatrix<S, SparseMatrix<S>>,
               shared_ptr<DelayedSparseMatrix<S, SparseMatrix<S>>>,
               DelayedSparseMatrix<S>>(m, "DelayedNormalSparseMatrix")
        .def_readwrite("mat", &DelayedSparseMatrix<S, SparseMatrix<S>>::mat)
        .def(py::init<const shared_ptr<SparseMatrix<S>> &>());

    py::class_<DelayedSparseMatrix<S, CSRSparseMatrix<S>>,
               shared_ptr<DelayedSparseMatrix<S, CSRSparseMatrix<S>>>,
               DelayedSparseMatrix<S>>(m, "DelayedCSRSparseMatrix")
        .def_readwrite("mat", &DelayedSparseMatrix<S, CSRSparseMatrix<S>>::mat)
        .def(py::init<const shared_ptr<CSRSparseMatrix<S>> &>());

    py::class_<DelayedSparseMatrix<S, OpExpr<S>>,
               shared_ptr<DelayedSparseMatrix<S, OpExpr<S>>>,
               DelayedSparseMatrix<S>>(m, "DelayedOpExprSparseMatrix")
        .def_readwrite("m", &DelayedSparseMatrix<S, OpExpr<S>>::m)
        .def_readwrite("op", &DelayedSparseMatrix<S, OpExpr<S>>::op)
        .def(py::init<uint16_t, const shared_ptr<OpExpr<S>> &>())
        .def(py::init<uint16_t, const shared_ptr<OpExpr<S>> &,
                      const shared_ptr<SparseMatrixInfo<S>> &>());

    py::class_<DelayedSparseMatrix<S, Hamiltonian<S>>,
               shared_ptr<DelayedSparseMatrix<S, Hamiltonian<S>>>,
               DelayedSparseMatrix<S, OpExpr<S>>>(m, "DelayedHamilSparseMatrix")
        .def_readwrite("hamil", &DelayedSparseMatrix<S, Hamiltonian<S>>::hamil)
        .def(py::init<const shared_ptr<Hamiltonian<S>> &, uint16_t,
                      const shared_ptr<OpExpr<S>> &>())
        .def(py::init<const shared_ptr<Hamiltonian<S>> &, uint16_t,
                      const shared_ptr<OpExpr<S>> &,
                      const shared_ptr<SparseMatrixInfo<S>> &>());

    py::class_<SparseTensor<S>, shared_ptr<SparseTensor<S>>>(m, "SparseTensor")
        .def(py::init<>())
        .def(py::init<
             const vector<vector<pair<pair<S, S>, shared_ptr<Tensor>>>> &>())
        .def_readwrite("data", &SparseTensor<S>::data)
        .def("__repr__", [](SparseTensor<S> *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });

    py::bind_vector<vector<pair<S, shared_ptr<SparseMatrixInfo<S>>>>>(
        m, "VectorPLMatInfo");
    py::bind_vector<vector<vector<pair<S, shared_ptr<SparseMatrixInfo<S>>>>>>(
        m, "VectorVectorPLMatInfo");
    py::bind_vector<vector<shared_ptr<SparseMatrixInfo<S>>>>(m,
                                                             "VectorSpMatInfo");
    py::bind_vector<vector<shared_ptr<SparseMatrix<S>>>>(m, "VectorSpMat");
    py::bind_vector<vector<map<OpNames, shared_ptr<SparseMatrix<S>>>>>(
        m, "VectorMapOpNamesSpMat");
    py::bind_map<unordered_map<OpNames, shared_ptr<SparseMatrix<S>>>>(
        m, "MapOpNamesSpMat");
    py::bind_map<
        unordered_map<shared_ptr<OpExpr<S>>, shared_ptr<SparseMatrix<S>>>>(
        m, "MapOpExprSpMat");

    py::bind_vector<vector<pair<pair<S, S>, shared_ptr<Tensor>>>>(
        m, "VectorPSSTensor");
    py::bind_vector<vector<vector<pair<pair<S, S>, shared_ptr<Tensor>>>>>(
        m, "VectorVectorPSSTensor");
    py::bind_vector<vector<shared_ptr<SparseTensor<S>>>>(m, "VectorSpTensor");

    py::class_<SparseMatrixGroup<S>, shared_ptr<SparseMatrixGroup<S>>>(
        m, "SparseMatrixGroup")
        .def(py::init<>())
        .def_readwrite("infos", &SparseMatrixGroup<S>::infos)
        .def_readwrite("offsets", &SparseMatrixGroup<S>::offsets)
        .def_readwrite("total_memory", &SparseMatrixGroup<S>::total_memory)
        .def_readwrite("n", &SparseMatrixGroup<S>::n)
        .def_property(
            "data",
            [](SparseMatrixGroup<S> *self) {
                return py::array_t<double>(self->total_memory, self->data);
            },
            [](SparseMatrixGroup<S> *self, const py::array_t<double> &v) {
                assert(v.size() == self->total_memory);
                memcpy(self->data, v.data(),
                       sizeof(double) * self->total_memory);
            })
        .def("load_data", &SparseMatrixGroup<S>::load_data, py::arg("filename"),
             py::arg("load_info") = false, py::arg("i_alloc") = nullptr)
        .def("save_data", &SparseMatrixGroup<S>::save_data, py::arg("filename"),
             py::arg("save_info") = false)
        .def("allocate",
             [](SparseMatrixGroup<S> *self,
                const vector<shared_ptr<SparseMatrixInfo<S>>> &infos) {
                 self->allocate(infos);
             })
        .def("deallocate", &SparseMatrixGroup<S>::deallocate)
        .def("deallocate_infos", &SparseMatrixGroup<S>::deallocate_infos)
        .def("delta_quanta", &SparseMatrixGroup<S>::delta_quanta)
        .def("randomize", &SparseMatrixGroup<S>::randomize, py::arg("a") = 0.0,
             py::arg("b") = 1.0)
        .def("norm", &SparseMatrixGroup<S>::norm)
        .def("iscale", &SparseMatrixGroup<S>::iscale, py::arg("d"))
        .def("normalize", &SparseMatrixGroup<S>::normalize)
        .def_static("normalize_all", &SparseMatrixGroup<S>::normalize_all)
        .def("left_svd",
             [](SparseMatrixGroup<S> *self) {
                 vector<S> qs;
                 vector<shared_ptr<Tensor>> s, r;
                 vector<vector<shared_ptr<Tensor>>> l;
                 self->left_svd(qs, l, s, r);
                 return make_tuple(qs, l, s, r);
             })
        .def("right_svd",
             [](SparseMatrixGroup<S> *self) {
                 vector<S> qs;
                 vector<shared_ptr<Tensor>> l, s;
                 vector<vector<shared_ptr<Tensor>>> r;
                 self->right_svd(qs, l, s, r);
                 return make_tuple(qs, l, s, r);
             })
        .def("__getitem__",
             [](SparseMatrixGroup<S> *self, int idx) { return (*self)[idx]; });

    py::bind_vector<vector<shared_ptr<SparseMatrixGroup<S>>>>(
        m, "VectorSpMatGroup");
}

template <typename S> void bind_mps(py::module &m) {
    py::class_<MPSInfo<S>, shared_ptr<MPSInfo<S>>>(m, "MPSInfo")
        .def_readwrite("n_sites", &MPSInfo<S>::n_sites)
        .def_readwrite("vacuum", &MPSInfo<S>::vacuum)
        .def_readwrite("target", &MPSInfo<S>::target)
        .def_readwrite("bond_dim", &MPSInfo<S>::bond_dim)
        .def_readwrite("basis", &MPSInfo<S>::basis)
        .def_readwrite("left_dims_fci", &MPSInfo<S>::left_dims_fci)
        .def_readwrite("right_dims_fci", &MPSInfo<S>::right_dims_fci)
        .def_readwrite("left_dims", &MPSInfo<S>::left_dims)
        .def_readwrite("right_dims", &MPSInfo<S>::right_dims)
        .def_readwrite("tag", &MPSInfo<S>::tag)
        .def(py::init<int>())
        .def(py::init<int, S, S, const vector<shared_ptr<StateInfo<S>>> &>())
        .def(py::init<int, S, S, const vector<shared_ptr<StateInfo<S>>> &,
                      bool>())
        .def("get_ancilla_type", &MPSInfo<S>::get_ancilla_type)
        .def("get_type", &MPSInfo<S>::get_type)
        .def("load_data",
             (void (MPSInfo<S>::*)(const string &)) & MPSInfo<S>::load_data)
        .def("save_data", (void (MPSInfo<S>::*)(const string &) const) &
                              MPSInfo<S>::save_data)
        .def("get_max_bond_dimension", &MPSInfo<S>::get_max_bond_dimension)
        .def("check_bond_dimensions", &MPSInfo<S>::check_bond_dimensions)
        .def("set_bond_dimension_using_occ",
             &MPSInfo<S>::set_bond_dimension_using_occ, py::arg("m"),
             py::arg("occ"), py::arg("bias") = 1.0)
        .def("set_bond_dimension_using_hf",
             &MPSInfo<S>::set_bond_dimension_using_hf, py::arg("m"),
             py::arg("occ"), py::arg("n_local") = 0)
        .def("set_bond_dimension_full_fci",
             &MPSInfo<S>::set_bond_dimension_full_fci,
             py::arg("left_vacuum") = S(S::invalid),
             py::arg("right_vacuum") = S(S::invalid))
        .def("set_bond_dimension_fci", &MPSInfo<S>::set_bond_dimension_fci,
             py::arg("left_vacuum") = S(S::invalid),
             py::arg("right_vacuum") = S(S::invalid))
        .def("set_bond_dimension", &MPSInfo<S>::set_bond_dimension)
        .def("swap_wfn_to_fused_left", &MPSInfo<S>::swap_wfn_to_fused_left)
        .def("swap_wfn_to_fused_right", &MPSInfo<S>::swap_wfn_to_fused_right)
        .def("get_filename", &MPSInfo<S>::get_filename, py::arg("left"),
             py::arg("i"), py::arg("dir") = "")
        .def("save_mutable", &MPSInfo<S>::save_mutable)
        .def("copy_mutable", &MPSInfo<S>::copy_mutable)
        .def("deallocate_mutable", &MPSInfo<S>::deallocate_mutable)
        .def("load_mutable", &MPSInfo<S>::load_mutable)
        .def("save_left_dims", &MPSInfo<S>::save_left_dims)
        .def("save_right_dims", &MPSInfo<S>::save_right_dims)
        .def("load_left_dims", &MPSInfo<S>::load_left_dims)
        .def("load_right_dims", &MPSInfo<S>::load_right_dims)
        .def("deep_copy", &MPSInfo<S>::deep_copy)
        .def("deallocate", &MPSInfo<S>::deallocate);

    py::class_<DynamicMPSInfo<S>, shared_ptr<DynamicMPSInfo<S>>, MPSInfo<S>>(
        m, "DynamicMPSInfo")
        .def_readwrite("iocc", &DynamicMPSInfo<S>::iocc)
        .def_readwrite("n_local", &DynamicMPSInfo<S>::n_local)
        .def(py::init([](int n_sites, S vacuum, S target,
                         const vector<shared_ptr<StateInfo<S>>> &basis,
                         const vector<uint8_t> &iocc) {
            return make_shared<DynamicMPSInfo<S>>(n_sites, vacuum, target,
                                                  basis, iocc);
        }))
        .def("set_left_bond_dimension_local",
             &DynamicMPSInfo<S>::set_left_bond_dimension_local, py::arg("i"),
             py::arg("match_prev") = false)
        .def("set_right_bond_dimension_local",
             &DynamicMPSInfo<S>::set_right_bond_dimension_local, py::arg("i"),
             py::arg("match_prev") = false);

    py::class_<CASCIMPSInfo<S>, shared_ptr<CASCIMPSInfo<S>>, MPSInfo<S>>(
        m, "CASCIMPSInfo")
        .def_readwrite("casci_mask", &CASCIMPSInfo<S>::casci_mask)
        .def(py::init([](int n_sites, S vacuum, S target,
                         const vector<shared_ptr<StateInfo<S>>> &basis,
                         const vector<ActiveTypes> &casci_mask) {
            return make_shared<CASCIMPSInfo<S>>(n_sites, vacuum, target, basis,
                                                casci_mask);
        }))
        .def(py::init([](int n_sites, S vacuum, S target,
                         const vector<shared_ptr<StateInfo<S>>> &basis,
                         int n_active_sites, int n_active_electrons) {
            return make_shared<CASCIMPSInfo<S>>(n_sites, vacuum, target, basis,
                                                n_active_sites,
                                                n_active_electrons);
        }));

    py::class_<MRCIMPSInfo<S>, shared_ptr<MRCIMPSInfo<S>>, MPSInfo<S>>(
        m, "MRCIMPSInfo")
        .def_readonly("n_ext", &MRCIMPSInfo<S>::n_ext,
                      "Number of external orbitals")
        .def_readonly("ci_order", &MRCIMPSInfo<S>::ci_order,
                      "Up to how many electrons are allowed in ext. orbitals: "
                      "2 gives MR-CISD")
        .def(py::init([](int n_sites, int n_ext, int ci_order, S vacuum,
                         S target,
                         const vector<shared_ptr<StateInfo<S>>> &basis) {
            return make_shared<MRCIMPSInfo<S>>(n_sites, n_ext, ci_order, vacuum,
                                               target, basis);
        }));

    py::class_<AncillaMPSInfo<S>, shared_ptr<AncillaMPSInfo<S>>, MPSInfo<S>>(
        m, "AncillaMPSInfo")
        .def_readwrite("n_physical_sites", &AncillaMPSInfo<S>::n_physical_sites)
        .def(py::init([](int n_sites, S vacuum, S target,
                         const vector<shared_ptr<StateInfo<S>>> &basis) {
            return make_shared<AncillaMPSInfo<S>>(n_sites, vacuum, target,
                                                  basis);
        }))
        .def_static("trans_basis", &AncillaMPSInfo<S>::trans_basis)
        .def("set_thermal_limit", &AncillaMPSInfo<S>::set_thermal_limit);

    py::class_<MultiMPSInfo<S>, shared_ptr<MultiMPSInfo<S>>, MPSInfo<S>>(
        m, "MultiMPSInfo")
        .def_readwrite("targets", &MultiMPSInfo<S>::targets)
        .def(py::init<int>())
        .def(py::init([](int n_sites, S vacuum, const vector<S> &target,
                         const vector<shared_ptr<StateInfo<S>>> &basis) {
            return make_shared<MultiMPSInfo<S>>(n_sites, vacuum, target, basis);
        }))
        .def("make_single", &MultiMPSInfo<S>::make_single)
        .def_static("from_mps_info", &MultiMPSInfo<S>::from_mps_info);

    py::class_<MPS<S>, shared_ptr<MPS<S>>>(m, "MPS")
        .def(py::init<const shared_ptr<MPSInfo<S>> &>())
        .def(py::init<int, int, int>())
        .def_readwrite("n_sites", &MPS<S>::n_sites)
        .def_readwrite("center", &MPS<S>::center)
        .def_readwrite("dot", &MPS<S>::dot)
        .def_readwrite("info", &MPS<S>::info)
        .def_readwrite("tensors", &MPS<S>::tensors)
        .def_readwrite("canonical_form", &MPS<S>::canonical_form)
        .def("get_type", &MPS<S>::get_type)
        .def("initialize", &MPS<S>::initialize, py::arg("info"),
             py::arg("init_left") = true, py::arg("init_right") = true)
        .def("fill_thermal_limit", &MPS<S>::fill_thermal_limit)
        .def("canonicalize", &MPS<S>::canonicalize)
        .def("random_canonicalize", &MPS<S>::random_canonicalize)
        .def("to_singlet_embedding_wfn", &MPS<S>::to_singlet_embedding_wfn,
             py::arg("cg"), py::arg("para_rule") = nullptr)
        .def("move_left", &MPS<S>::move_left, py::arg("cg"),
             py::arg("para_rule") = nullptr)
        .def("move_right", &MPS<S>::move_right, py::arg("cg"),
             py::arg("para_rule") = nullptr)
        .def("flip_fused_form", &MPS<S>::flip_fused_form)
        .def("get_filename", &MPS<S>::get_filename, py::arg("i"),
             py::arg("dir") = "")
        .def("load_data", &MPS<S>::load_data)
        .def("save_data", &MPS<S>::save_data)
        .def("copy_data", &MPS<S>::copy_data)
        .def("load_mutable", &MPS<S>::load_mutable)
        .def("save_mutable", &MPS<S>::save_mutable)
        .def("save_tensor", &MPS<S>::save_tensor)
        .def("load_tensor", &MPS<S>::load_tensor)
        .def("unload_tensor", &MPS<S>::unload_tensor)
        .def("deep_copy", &MPS<S>::deep_copy)
        .def("estimate_storage", &MPS<S>::estimate_storage,
             py::arg("info") = nullptr)
        .def("deallocate", &MPS<S>::deallocate);

    py::bind_vector<vector<shared_ptr<MPS<S>>>>(m, "VectorMPS");

    py::class_<MultiMPS<S>, shared_ptr<MultiMPS<S>>, MPS<S>>(m, "MultiMPS")
        .def(py::init<const shared_ptr<MultiMPSInfo<S>> &>())
        .def(py::init<int, int, int, int>())
        .def_readwrite("nroots", &MultiMPS<S>::nroots)
        .def_readwrite("wfns", &MultiMPS<S>::wfns)
        .def_readwrite("weights", &MultiMPS<S>::weights)
        .def("get_wfn_filename", &MultiMPS<S>::get_wfn_filename)
        .def("save_wavefunction", &MultiMPS<S>::save_wavefunction)
        .def("load_wavefunction", &MultiMPS<S>::load_wavefunction)
        .def("unload_wavefunction", &MultiMPS<S>::unload_wavefunction)
        .def("extract", &MultiMPS<S>::extract)
        .def("iscale", &MultiMPS<S>::iscale)
        .def("make_single", &MultiMPS<S>::make_single)
        .def_static("make_complex", &MultiMPS<S>::make_complex);

    py::class_<ParallelMPS<S>, shared_ptr<ParallelMPS<S>>, MPS<S>>(
        m, "ParallelMPS")
        .def(py::init<const shared_ptr<MPSInfo<S>> &>())
        .def(py::init<int, int, int>())
        .def(py::init<const shared_ptr<MPS<S>> &>())
        .def(py::init<const shared_ptr<MPSInfo<S>> &,
                      const shared_ptr<ParallelRule<S>> &>())
        .def(py::init<int, int, int, const shared_ptr<ParallelRule<S>> &>())
        .def(py::init<const shared_ptr<MPS<S>> &,
                      const shared_ptr<ParallelRule<S>> &>())
        .def_readwrite("conn_centers", &ParallelMPS<S>::conn_centers)
        .def_readwrite("conn_matrices", &ParallelMPS<S>::conn_matrices)
        .def_readwrite("ncenter", &ParallelMPS<S>::ncenter)
        .def_readwrite("ncenter", &ParallelMPS<S>::ncenter)
        .def_readwrite("ncenter", &ParallelMPS<S>::ncenter)
        .def_readwrite("svd_eps", &ParallelMPS<S>::svd_eps)
        .def_readwrite("svd_cutoff", &ParallelMPS<S>::svd_cutoff);

    py::class_<UnfusedMPS<S>, shared_ptr<UnfusedMPS<S>>>(m, "UnfusedMPS")
        .def(py::init<>())
        .def(py::init<const shared_ptr<MPS<S>> &>())
        .def_readwrite("info", &UnfusedMPS<S>::info)
        .def_readwrite("tensors", &UnfusedMPS<S>::tensors)
        .def_readwrite("n_sites", &UnfusedMPS<S>::n_sites)
        .def_readwrite("center", &UnfusedMPS<S>::center)
        .def_readwrite("dot", &UnfusedMPS<S>::dot)
        .def_readwrite("canonical_form", &UnfusedMPS<S>::canonical_form)
        .def_static("forward_left_fused", &UnfusedMPS<S>::forward_left_fused,
                    py::arg("i"), py::arg("mps"), py::arg("wfn"))
        .def_static("forward_right_fused", &UnfusedMPS<S>::forward_right_fused,
                    py::arg("i"), py::arg("mps"), py::arg("wfn"))
        .def_static("forward_mps_tensor", &UnfusedMPS<S>::forward_mps_tensor,
                    py::arg("i"), py::arg("mps"))
        .def_static("backward_left_fused", &UnfusedMPS<S>::backward_left_fused,
                    py::arg("i"), py::arg("mps"), py::arg("spt"),
                    py::arg("wfn"))
        .def_static("backward_right_fused",
                    &UnfusedMPS<S>::backward_right_fused, py::arg("i"),
                    py::arg("mps"), py::arg("spt"), py::arg("wfn"))
        .def_static("backward_mps_tensor", &UnfusedMPS<S>::backward_mps_tensor,
                    py::arg("i"), py::arg("mps"), py::arg("spt"))
        .def("initialize", &UnfusedMPS<S>::initialize)
        .def("finalize", &UnfusedMPS<S>::finalize);

    py::class_<DeterminantTRIE<S>, shared_ptr<DeterminantTRIE<S>>>(
        m, "DeterminantTRIE")
        .def(py::init<int>(), py::arg("n_sites"))
        .def(py::init<int, bool>(), py::arg("n_sites"),
             py::arg("enable_look_up"))
        .def_readwrite("data", &DeterminantTRIE<S>::data)
        .def_readwrite("dets", &DeterminantTRIE<S>::dets)
        .def_readwrite("invs", &DeterminantTRIE<S>::invs)
        .def_readwrite("vals", &DeterminantTRIE<S>::vals)
        .def_readwrite("n_sites", &DeterminantTRIE<S>::n_sites)
        .def_readwrite("enable_look_up", &DeterminantTRIE<S>::enable_look_up)
        .def("clear", &DeterminantTRIE<S>::clear)
        .def("copy", &DeterminantTRIE<S>::copy)
        .def("__len__", &DeterminantTRIE<S>::size)
        .def("append", &DeterminantTRIE<S>::push_back, py::arg("det"))
        .def("find", &DeterminantTRIE<S>::find, py::arg("det"))
        .def("__getitem__", &DeterminantTRIE<S>::operator[], py::arg("idx"))
        .def("get_state_occupation", &DeterminantTRIE<S>::get_state_occupation)
        .def("evaluate", &DeterminantTRIE<S>::evaluate, py::arg("mps"),
             py::arg("cutoff") = 0.0);
}

template <typename S> void bind_operator(py::module &m) {
    py::class_<OperatorFunctions<S>, shared_ptr<OperatorFunctions<S>>>(
        m, "OperatorFunctions")
        .def_readwrite("cg", &OperatorFunctions<S>::cg)
        .def_readwrite("seq", &OperatorFunctions<S>::seq)
        .def(py::init<const shared_ptr<CG<S>> &>())
        .def("iadd", &OperatorFunctions<S>::iadd, py::arg("a"), py::arg("b"),
             py::arg("scale") = 1.0, py::arg("conj") = false)
        .def("tensor_rotate", &OperatorFunctions<S>::tensor_rotate,
             py::arg("a"), py::arg("c"), py::arg("rot_bra"), py::arg("rot_ket"),
             py::arg("trans"), py::arg("scale") = 1.0)
        .def("tensor_product_diagonal",
             &OperatorFunctions<S>::tensor_product_diagonal, py::arg("conj"),
             py::arg("a"), py::arg("b"), py::arg("c"), py::arg("opdq"),
             py::arg("scale") = 1.0)
        .def("tensor_partial_expectation",
             &OperatorFunctions<S>::tensor_partial_expectation, py::arg("conj"),
             py::arg("a"), py::arg("b"), py::arg("c"), py::arg("v"),
             py::arg("opdq"), py::arg("scale") = 1.0)
        .def("tensor_product_multiply",
             &OperatorFunctions<S>::tensor_product_multiply, py::arg("conj"),
             py::arg("a"), py::arg("b"), py::arg("c"), py::arg("v"),
             py::arg("opdq"), py::arg("scale") = 1.0,
             py::arg("tt") = TraceTypes::None)
        .def("tensor_product", &OperatorFunctions<S>::tensor_product,
             py::arg("conj"), py::arg("a"), py::arg("b"), py::arg("c"),
             py::arg("scale") = 1.0)
        .def("product", &OperatorFunctions<S>::product, py::arg("a"),
             py::arg("conj"), py::arg("b"), py::arg("c"),
             py::arg("scale") = 1.0)
        .def_static("trans_product", &OperatorFunctions<S>::trans_product,
                    py::arg("a"), py::arg("b"), py::arg("trace_right"),
                    py::arg("noise") = 0.0,
                    py::arg("noise_type") = NoiseTypes::DensityMatrix);

    py::class_<CSROperatorFunctions<S>, shared_ptr<CSROperatorFunctions<S>>,
               OperatorFunctions<S>>(m, "CSROperatorFunctions")
        .def(py::init<const shared_ptr<CG<S>> &>());

    py::class_<OperatorTensor<S>, shared_ptr<OperatorTensor<S>>>(
        m, "OperatorTensor")
        .def(py::init<>())
        .def_readwrite("lmat", &OperatorTensor<S>::lmat)
        .def_readwrite("rmat", &OperatorTensor<S>::rmat)
        .def_readwrite("ops", &OperatorTensor<S>::ops)
        .def("get_type", &OperatorTensor<S>::get_type)
        .def("reallocate", &OperatorTensor<S>::reallocate, py::arg("clean"))
        .def("deallocate", &OperatorTensor<S>::deallocate)
        .def("copy", &OperatorTensor<S>::copy)
        .def("deep_copy", &OperatorTensor<S>::deep_copy,
             py::arg("alloc") = nullptr);

    py::class_<DelayedOperatorTensor<S>, shared_ptr<DelayedOperatorTensor<S>>,
               OperatorTensor<S>>(m, "DelayedOperatorTensor")
        .def(py::init<>())
        .def_readwrite("dops", &DelayedOperatorTensor<S>::dops)
        .def_readwrite("mat", &DelayedOperatorTensor<S>::mat)
        .def_readwrite("lopt", &DelayedOperatorTensor<S>::lopt)
        .def_readwrite("ropt", &DelayedOperatorTensor<S>::ropt);

    py::bind_vector<vector<shared_ptr<OperatorTensor<S>>>>(m, "VectorOpTensor");

    py::class_<TensorFunctions<S>, shared_ptr<TensorFunctions<S>>>(
        m, "TensorFunctions")
        .def(py::init<const shared_ptr<OperatorFunctions<S>> &>())
        .def_readwrite("opf", &TensorFunctions<S>::opf)
        .def("get_type", &TensorFunctions<S>::get_type)
        .def("left_assign", &TensorFunctions<S>::left_assign, py::arg("a"),
             py::arg("c"))
        .def("right_assign", &TensorFunctions<S>::right_assign, py::arg("a"),
             py::arg("c"))
        .def("left_contract", &TensorFunctions<S>::left_contract, py::arg("a"),
             py::arg("b"), py::arg("c"), py::arg("cexprs") = nullptr,
             py::arg("delayed") = OpNamesSet())
        .def("right_contract", &TensorFunctions<S>::right_contract,
             py::arg("a"), py::arg("b"), py::arg("c"),
             py::arg("cexprs") = nullptr, py::arg("delayed") = OpNamesSet())
        .def("tensor_product_multi_multiply",
             &TensorFunctions<S>::tensor_product_multi_multiply)
        .def("tensor_product_multiply",
             &TensorFunctions<S>::tensor_product_multiply)
        .def("tensor_product_diagonal",
             &TensorFunctions<S>::tensor_product_diagonal)
        .def("tensor_product", &TensorFunctions<S>::tensor_product)
        .def("delayed_left_contract",
             &TensorFunctions<S>::delayed_left_contract)
        .def("delayed_right_contract",
             &TensorFunctions<S>::delayed_right_contract)
        .def("left_rotate", &TensorFunctions<S>::left_rotate)
        .def("right_rotate", &TensorFunctions<S>::right_rotate)
        .def("intermediates", &TensorFunctions<S>::intermediates)
        .def("numerical_transform", &TensorFunctions<S>::numerical_transform)
        .def("post_numerical_transform",
             &TensorFunctions<S>::post_numerical_transform)
        .def("substitute_delayed_exprs",
             &TensorFunctions<S>::substitute_delayed_exprs)
        .def("delayed_contract",
             (shared_ptr<DelayedOperatorTensor<S>>(TensorFunctions<S>::*)(
                 const shared_ptr<OperatorTensor<S>> &,
                 const shared_ptr<OperatorTensor<S>> &,
                 const shared_ptr<OpExpr<S>> &, OpNamesSet delayed) const) &
                 TensorFunctions<S>::delayed_contract)
        .def("delayed_contract_simplified",
             (shared_ptr<DelayedOperatorTensor<S>>(TensorFunctions<S>::*)(
                 const shared_ptr<OperatorTensor<S>> &,
                 const shared_ptr<OperatorTensor<S>> &,
                 const shared_ptr<Symbolic<S>> &,
                 const shared_ptr<Symbolic<S>> &, OpNamesSet delayed) const) &
                 TensorFunctions<S>::delayed_contract);

    py::class_<ArchivedTensorFunctions<S>,
               shared_ptr<ArchivedTensorFunctions<S>>, TensorFunctions<S>>(
        m, "ArchivedTensorFunctions")
        .def(py::init<const shared_ptr<OperatorFunctions<S>> &>())
        .def_readwrite("filename", &ArchivedTensorFunctions<S>::filename)
        .def_readwrite("offset", &ArchivedTensorFunctions<S>::offset)
        .def("archive_tensor", &ArchivedTensorFunctions<S>::archive_tensor,
             py::arg("a"));

    py::class_<DelayedTensorFunctions<S>, shared_ptr<DelayedTensorFunctions<S>>,
               TensorFunctions<S>>(m, "DelayedTensorFunctions")
        .def(py::init<const shared_ptr<OperatorFunctions<S>> &>());
}

template <typename S> void bind_partition(py::module &m) {

    py::class_<Partition<S>, shared_ptr<Partition<S>>>(m, "Partition")
        .def(py::init<const shared_ptr<OperatorTensor<S>> &,
                      const shared_ptr<OperatorTensor<S>> &,
                      const shared_ptr<OperatorTensor<S>> &>())
        .def(py::init<const shared_ptr<OperatorTensor<S>> &,
                      const shared_ptr<OperatorTensor<S>> &,
                      const shared_ptr<OperatorTensor<S>> &,
                      const shared_ptr<OperatorTensor<S>> &>())
        .def_readwrite("left", &Partition<S>::left)
        .def_readwrite("right", &Partition<S>::right)
        .def_readwrite("middle", &Partition<S>::middle)
        .def_readwrite("left_op_infos", &Partition<S>::left_op_infos)
        .def_readwrite("right_op_infos", &Partition<S>::right_op_infos)
        .def("load_data", (void (Partition<S>::*)(bool, const string &)) &
                              Partition<S>::load_data)
        .def("save_data", (void (Partition<S>::*)(bool, const string &) const) &
                              Partition<S>::save_data)
        .def_static("find_op_info", &Partition<S>::find_op_info)
        .def_static("build_left", &Partition<S>::build_left)
        .def_static("build_right", &Partition<S>::build_right)
        .def_static("get_uniq_labels", &Partition<S>::get_uniq_labels)
        .def_static("get_uniq_sub_labels", &Partition<S>::get_uniq_sub_labels)
        .def_static("deallocate_op_infos_notrunc",
                    &Partition<S>::deallocate_op_infos_notrunc)
        .def_static("copy_op_infos", &Partition<S>::copy_op_infos)
        .def_static("init_left_op_infos", &Partition<S>::init_left_op_infos)
        .def_static("init_left_op_infos_notrunc",
                    &Partition<S>::init_left_op_infos_notrunc)
        .def_static("init_right_op_infos", &Partition<S>::init_right_op_infos)
        .def_static("init_right_op_infos_notrunc",
                    &Partition<S>::init_right_op_infos_notrunc);

    py::bind_vector<vector<shared_ptr<Partition<S>>>>(m, "VectorPartition");

    py::class_<EffectiveHamiltonian<S>, shared_ptr<EffectiveHamiltonian<S>>>(
        m, "EffectiveHamiltonian")
        .def(py::init<const vector<pair<S, shared_ptr<SparseMatrixInfo<S>>>> &,
                      const vector<pair<S, shared_ptr<SparseMatrixInfo<S>>>> &,
                      const shared_ptr<DelayedOperatorTensor<S>> &,
                      const shared_ptr<SparseMatrix<S>> &,
                      const shared_ptr<SparseMatrix<S>> &,
                      const shared_ptr<OpElement<S>> &,
                      const shared_ptr<SymbolicColumnVector<S>> &,
                      const shared_ptr<TensorFunctions<S>> &, bool>())
        .def_readwrite("left_op_infos", &EffectiveHamiltonian<S>::left_op_infos)
        .def_readwrite("right_op_infos",
                       &EffectiveHamiltonian<S>::right_op_infos)
        .def_readwrite("op", &EffectiveHamiltonian<S>::op)
        .def_readwrite("bra", &EffectiveHamiltonian<S>::bra)
        .def_readwrite("ket", &EffectiveHamiltonian<S>::ket)
        .def_readwrite("diag", &EffectiveHamiltonian<S>::diag)
        .def_readwrite("cmat", &EffectiveHamiltonian<S>::cmat)
        .def_readwrite("vmat", &EffectiveHamiltonian<S>::vmat)
        .def_readwrite("tf", &EffectiveHamiltonian<S>::tf)
        .def_readwrite("opdq", &EffectiveHamiltonian<S>::opdq)
        .def_readwrite("compute_diag", &EffectiveHamiltonian<S>::compute_diag)
        .def("__call__", &EffectiveHamiltonian<S>::operator(), py::arg("b"),
             py::arg("c"), py::arg("idx") = 0, py::arg("factor") = 1.0,
             py::arg("all_reduce") = true)
        .def("eigs", &EffectiveHamiltonian<S>::eigs)
        .def("multiply", &EffectiveHamiltonian<S>::multiply)
        .def("inverse_multiply", &EffectiveHamiltonian<S>::inverse_multiply)
        .def("greens_function", &EffectiveHamiltonian<S>::greens_function)
        .def("expect", &EffectiveHamiltonian<S>::expect)
        .def("rk4_apply", &EffectiveHamiltonian<S>::rk4_apply, py::arg("beta"),
             py::arg("const_e"), py::arg("eval_energy") = false,
             py::arg("para_rule") = nullptr)
        .def("expo_apply", &EffectiveHamiltonian<S>::expo_apply,
             py::arg("beta"), py::arg("const_e"), py::arg("symmetric"),
             py::arg("iprint") = false, py::arg("para_rule") = nullptr)
        .def("deallocate", &EffectiveHamiltonian<S>::deallocate);

    py::bind_vector<vector<shared_ptr<EffectiveHamiltonian<S>>>>(
        m, "VectorEffectiveHamiltonian");

    py::class_<LinearEffectiveHamiltonian<S>,
               shared_ptr<LinearEffectiveHamiltonian<S>>>(
        m, "LinearEffectiveHamiltonian")
        .def(py::init<const shared_ptr<EffectiveHamiltonian<S>> &>())
        .def(py::init<const vector<shared_ptr<EffectiveHamiltonian<S>>> &,
                      const vector<double> &>())
        .def("__call__", &LinearEffectiveHamiltonian<S>::operator(),
             py::arg("b"), py::arg("c"))
        .def("eigs", &LinearEffectiveHamiltonian<S>::eigs)
        .def("deallocate", &LinearEffectiveHamiltonian<S>::deallocate)
        .def_readwrite("h_effs", &LinearEffectiveHamiltonian<S>::h_effs)
        .def_readwrite("coeffs", &LinearEffectiveHamiltonian<S>::coeffs)
        .def("__mul__",
             [](const shared_ptr<LinearEffectiveHamiltonian<S>> &self,
                double d) { return self * d; })
        .def("__rmul__",
             [](const shared_ptr<LinearEffectiveHamiltonian<S>> &self,
                double d) { return self * d; })
        .def("__neg__",
             [](const shared_ptr<LinearEffectiveHamiltonian<S>> &self) {
                 return -self;
             })
        .def("__add__",
             [](const shared_ptr<LinearEffectiveHamiltonian<S>> &self,
                const shared_ptr<LinearEffectiveHamiltonian<S>> &other) {
                 return self + other;
             })
        .def("__sub__",
             [](const shared_ptr<LinearEffectiveHamiltonian<S>> &self,
                const shared_ptr<LinearEffectiveHamiltonian<S>> &other) {
                 return self - other;
             });

    py::class_<EffectiveHamiltonian<S, MultiMPS<S>>,
               shared_ptr<EffectiveHamiltonian<S, MultiMPS<S>>>>(
        m, "EffectiveHamiltonianMultiMPS")
        .def(py::init<const vector<pair<S, shared_ptr<SparseMatrixInfo<S>>>> &,
                      const vector<pair<S, shared_ptr<SparseMatrixInfo<S>>>> &,
                      const shared_ptr<DelayedOperatorTensor<S>> &,
                      const vector<shared_ptr<SparseMatrixGroup<S>>> &,
                      const vector<shared_ptr<SparseMatrixGroup<S>>> &,
                      const shared_ptr<OpElement<S>> &,
                      const shared_ptr<SymbolicColumnVector<S>> &,
                      const shared_ptr<TensorFunctions<S>> &, bool>())
        .def_readwrite("left_op_infos",
                       &EffectiveHamiltonian<S, MultiMPS<S>>::left_op_infos)
        .def_readwrite("right_op_infos",
                       &EffectiveHamiltonian<S, MultiMPS<S>>::right_op_infos)
        .def_readwrite("op", &EffectiveHamiltonian<S, MultiMPS<S>>::op)
        .def_readwrite("bra", &EffectiveHamiltonian<S, MultiMPS<S>>::bra)
        .def_readwrite("ket", &EffectiveHamiltonian<S, MultiMPS<S>>::ket)
        .def_readwrite("diag", &EffectiveHamiltonian<S, MultiMPS<S>>::diag)
        .def_readwrite("cmat", &EffectiveHamiltonian<S, MultiMPS<S>>::cmat)
        .def_readwrite("vmat", &EffectiveHamiltonian<S, MultiMPS<S>>::vmat)
        .def_readwrite("tf", &EffectiveHamiltonian<S, MultiMPS<S>>::tf)
        .def_readwrite("opdq", &EffectiveHamiltonian<S, MultiMPS<S>>::opdq)
        .def_readwrite("compute_diag",
                       &EffectiveHamiltonian<S, MultiMPS<S>>::compute_diag)
        .def("__call__", &EffectiveHamiltonian<S, MultiMPS<S>>::operator(),
             py::arg("b"), py::arg("c"), py::arg("idx") = 0,
             py::arg("factor") = 1.0, py::arg("all_reduce") = true)
        .def("eigs", &EffectiveHamiltonian<S, MultiMPS<S>>::eigs)
        .def("expect", &EffectiveHamiltonian<S, MultiMPS<S>>::expect)
        .def("rk4_apply", &EffectiveHamiltonian<S, MultiMPS<S>>::rk4_apply,
             py::arg("beta"), py::arg("const_e"),
             py::arg("eval_energy") = false, py::arg("para_rule") = nullptr)
        .def("expo_apply", &EffectiveHamiltonian<S, MultiMPS<S>>::expo_apply,
             py::arg("beta"), py::arg("const_e"), py::arg("iprint") = false,
             py::arg("para_rule") = nullptr)
        .def("deallocate", &EffectiveHamiltonian<S, MultiMPS<S>>::deallocate);

    py::class_<MovingEnvironment<S>, shared_ptr<MovingEnvironment<S>>>(
        m, "MovingEnvironment")
        .def(py::init<const shared_ptr<MPO<S>> &, const shared_ptr<MPS<S>> &,
                      const shared_ptr<MPS<S>> &>())
        .def(py::init<const shared_ptr<MPO<S>> &, const shared_ptr<MPS<S>> &,
                      const shared_ptr<MPS<S>> &, const string &>())
        .def_readwrite("n_sites", &MovingEnvironment<S>::n_sites)
        .def_readwrite("center", &MovingEnvironment<S>::center)
        .def_readwrite("dot", &MovingEnvironment<S>::dot)
        .def_readwrite("mpo", &MovingEnvironment<S>::mpo)
        .def_readwrite("bra", &MovingEnvironment<S>::bra)
        .def_readwrite("ket", &MovingEnvironment<S>::ket)
        .def_readwrite("envs", &MovingEnvironment<S>::envs)
        .def_readwrite("tag", &MovingEnvironment<S>::tag)
        .def_readwrite("para_rule", &MovingEnvironment<S>::para_rule)
        .def_readwrite("tctr", &MovingEnvironment<S>::tctr)
        .def_readwrite("trot", &MovingEnvironment<S>::trot)
        .def_readwrite("iprint", &MovingEnvironment<S>::iprint)
        .def_readwrite("delayed_contraction",
                       &MovingEnvironment<S>::delayed_contraction)
        .def_readwrite("fuse_center", &MovingEnvironment<S>::fuse_center)
        .def_readwrite("save_partition_info",
                       &MovingEnvironment<S>::save_partition_info)
        .def_readwrite("cached_opt", &MovingEnvironment<S>::cached_opt)
        .def_readwrite("cached_info", &MovingEnvironment<S>::cached_info)
        .def_readwrite("cached_contraction",
                       &MovingEnvironment<S>::cached_contraction)
        .def("left_contract_rotate",
             &MovingEnvironment<S>::left_contract_rotate)
        .def("right_contract_rotate",
             &MovingEnvironment<S>::right_contract_rotate)
        .def("left_contract_rotate_unordered",
             &MovingEnvironment<S>::left_contract_rotate_unordered)
        .def("right_contract_rotate_unordered",
             &MovingEnvironment<S>::right_contract_rotate_unordered)
        .def("parallelize_mps", &MovingEnvironment<S>::parallelize_mps)
        .def("serialize_mps", &MovingEnvironment<S>::serialize_mps)
        .def(
            "left_contract",
            [](MovingEnvironment<S> *self, int iL,
               vector<pair<S, shared_ptr<SparseMatrixInfo<S>>>> &left_op_info) {
                shared_ptr<OperatorTensor<S>> new_left = nullptr;
                self->left_contract(iL, left_op_info, new_left, false);
                return new_left;
            })
        .def("right_contract",
             [](MovingEnvironment<S> *self, int iR,
                vector<pair<S, shared_ptr<SparseMatrixInfo<S>>>>
                    &right_op_infos) {
                 shared_ptr<OperatorTensor<S>> new_right = nullptr;
                 self->right_contract(iR, right_op_infos, new_right, false);
                 return new_right;
             })
        .def(
            "left_copy",
            [](MovingEnvironment<S> *self, int iL,
               vector<pair<S, shared_ptr<SparseMatrixInfo<S>>>> &left_op_info) {
                shared_ptr<OperatorTensor<S>> new_left = nullptr;
                self->left_copy(iL, left_op_info, new_left);
                return new_left;
            })
        .def("right_copy",
             [](MovingEnvironment<S> *self, int iR,
                vector<pair<S, shared_ptr<SparseMatrixInfo<S>>>>
                    &right_op_infos) {
                 shared_ptr<OperatorTensor<S>> new_right = nullptr;
                 self->right_copy(iR, right_op_infos, new_right);
                 return new_right;
             })
        .def("init_environments", &MovingEnvironment<S>::init_environments,
             py::arg("iprint") = false)
        .def("finalize_environments",
             &MovingEnvironment<S>::finalize_environments,
             py::arg("renormalize_ops") = true)
        .def("prepare", &MovingEnvironment<S>::prepare)
        .def("move_to", &MovingEnvironment<S>::move_to, py::arg("i"),
             py::arg("preserve_data") = false)
        .def("partial_prepare", &MovingEnvironment<S>::partial_prepare)
        .def("get_left_archive_filename",
             &MovingEnvironment<S>::get_left_archive_filename)
        .def("get_middle_archive_filename",
             &MovingEnvironment<S>::get_middle_archive_filename)
        .def("get_right_archive_filename",
             &MovingEnvironment<S>::get_right_archive_filename)
        .def("get_left_partition_filename",
             &MovingEnvironment<S>::get_left_partition_filename)
        .def("get_right_partition_filename",
             &MovingEnvironment<S>::get_right_partition_filename)
        .def("eff_ham", &MovingEnvironment<S>::eff_ham, py::arg("fuse_type"),
             py::arg("forward"), py::arg("compute_diag"), py::arg("bra_wfn"),
             py::arg("ket_wfn"))
        .def("multi_eff_ham", &MovingEnvironment<S>::multi_eff_ham,
             py::arg("fuse_type"), py::arg("forward"), py::arg("compute_diag"))
        .def_static("contract_two_dot", &MovingEnvironment<S>::contract_two_dot,
                    py::arg("i"), py::arg("mps"), py::arg("reduced") = false)
        .def_static("wavefunction_add_noise",
                    &MovingEnvironment<S>::wavefunction_add_noise,
                    py::arg("psi"), py::arg("noise"))
        .def_static("scale_perturbative_noise",
                    &MovingEnvironment<S>::scale_perturbative_noise,
                    py::arg("noise"), py::arg("noise_type"), py::arg("mats"))
        .def_static("density_matrix", &MovingEnvironment<S>::density_matrix,
                    py::arg("vacuum"), py::arg("psi"), py::arg("trace_right"),
                    py::arg("noise"), py::arg("noise_type"),
                    py::arg("scale") = 1.0, py::arg("pkets") = nullptr)
        .def_static("density_matrix_with_multi_target",
                    &MovingEnvironment<S>::density_matrix_with_multi_target,
                    py::arg("vacuum"), py::arg("psi"), py::arg("weights"),
                    py::arg("trace_right"), py::arg("noise"),
                    py::arg("noise_type"), py::arg("scale") = 1.0,
                    py::arg("pkets") = nullptr)
        .def_static("density_matrix_add_wfn",
                    &MovingEnvironment<S>::density_matrix_add_wfn)
        .def_static(
            "density_matrix_add_perturbative_noise",
            &MovingEnvironment<S>::density_matrix_add_perturbative_noise)
        .def_static("density_matrix_add_matrices",
                    &MovingEnvironment<S>::density_matrix_add_matrices)
        .def_static("density_matrix_add_matrix_groups",
                    &MovingEnvironment<S>::density_matrix_add_matrix_groups)
        .def_static("truncate_density_matrix",
                    [](const shared_ptr<SparseMatrix<S>> &dm, int k,
                       double cutoff, TruncationTypes trunc_type) {
                        vector<pair<int, int>> ss;
                        double error =
                            MovingEnvironment<S>::truncate_density_matrix(
                                dm, ss, k, cutoff, trunc_type);
                        return make_pair(error, ss);
                    })
        .def_static("truncate_singular_values",
                    [](const vector<S> &qs, const vector<shared_ptr<Tensor>> &s,
                       int k, double cutoff, TruncationTypes trunc_type) {
                        vector<pair<int, int>> ss;
                        double error =
                            MovingEnvironment<S>::truncate_singular_values(
                                qs, s, ss, k, cutoff, trunc_type);
                        return make_pair(error, ss);
                    })
        .def_static("rotation_matrix_info_from_svd",
                    &MovingEnvironment<S>::rotation_matrix_info_from_svd,
                    py::arg("opdq"), py::arg("qs"), py::arg("ts"),
                    py::arg("trace_right"), py::arg("ilr"), py::arg("im"))
        .def_static(
            "wavefunction_info_from_svd",
            [](const vector<S> &qs,
               const shared_ptr<SparseMatrixInfo<S>> &wfninfo, bool trace_right,
               const vector<int> &ilr, const vector<ubond_t> &im) {
                vector<vector<int>> idx_dm_to_wfn;
                shared_ptr<SparseMatrixInfo<S>> r =
                    MovingEnvironment<S>::wavefunction_info_from_svd(
                        qs, wfninfo, trace_right, ilr, im, idx_dm_to_wfn);
                return make_pair(r, idx_dm_to_wfn);
            })
        .def_static(
            "rotation_matrix_info_from_density_matrix",
            &MovingEnvironment<S>::rotation_matrix_info_from_density_matrix,
            py::arg("dminfo"), py::arg("trace_right"), py::arg("ilr"),
            py::arg("im"))
        .def_static(
            "wavefunction_info_from_density_matrix",
            [](const shared_ptr<SparseMatrixInfo<S>> &dminfo,
               const shared_ptr<SparseMatrixInfo<S>> &wfninfo, bool trace_right,
               const vector<int> &ilr, const vector<ubond_t> &im) {
                vector<vector<int>> idx_dm_to_wfn;
                shared_ptr<SparseMatrixInfo<S>> r =
                    MovingEnvironment<S>::wavefunction_info_from_density_matrix(
                        dminfo, wfninfo, trace_right, ilr, im, idx_dm_to_wfn);
                return make_pair(r, idx_dm_to_wfn);
            })
        .def_static(
            "split_density_matrix",
            [](const shared_ptr<SparseMatrix<S>> &dm,
               const shared_ptr<SparseMatrix<S>> &wfn, int k, bool trace_right,
               bool normalize, double cutoff, TruncationTypes trunc_type) {
                shared_ptr<SparseMatrix<S>> left = nullptr, right = nullptr;
                double error = MovingEnvironment<S>::split_density_matrix(
                    dm, wfn, k, trace_right, normalize, left, right, cutoff,
                    trunc_type);
                return make_tuple(error, left, right);
            },
            py::arg("dm"), py::arg("wfn"), py::arg("k"), py::arg("trace_right"),
            py::arg("normalize"), py::arg("cutoff"),
            py::arg("trunc_type") = TruncationTypes::Physical)
        .def_static(
            "split_wavefunction_svd",
            [](S opdq, const shared_ptr<SparseMatrix<S>> &wfn, int k,
               bool trace_right, bool normalize, double cutoff,
               TruncationTypes trunc_type, DecompositionTypes decomp_type) {
                shared_ptr<SparseMatrix<S>> left = nullptr, right = nullptr;
                double error = MovingEnvironment<S>::split_wavefunction_svd(
                    opdq, wfn, k, trace_right, normalize, left, right, cutoff,
                    trunc_type, decomp_type);
                return make_tuple(error, left, right);
            },
            py::arg("opdq"), py::arg("wfn"), py::arg("k"),
            py::arg("trace_right"), py::arg("normalize"), py::arg("cutoff"),
            py::arg("decomp_type") = DecompositionTypes::PureSVD,
            py::arg("trunc_type") = TruncationTypes::Physical)
        .def_static("propagate_wfn", &MovingEnvironment<S>::propagate_wfn,
                    py::arg("i"), py::arg("n_sites"), py::arg("mps"),
                    py::arg("forward"), py::arg("cg"))
        .def_static("contract_multi_two_dot",
                    &MovingEnvironment<S>::contract_multi_two_dot, py::arg("i"),
                    py::arg("mps"), py::arg("reduced") = false)
        .def_static(
            "multi_split_density_matrix",
            [](const shared_ptr<SparseMatrix<S>> &dm,
               const vector<shared_ptr<SparseMatrixGroup<S>>> &wfns, int k,
               bool trace_right, bool normalize, double cutoff,
               TruncationTypes trunc_type) {
                vector<shared_ptr<SparseMatrixGroup<S>>> new_wfns;
                shared_ptr<SparseMatrix<S>> rot_mat = nullptr;
                double error = MovingEnvironment<S>::multi_split_density_matrix(
                    dm, wfns, k, trace_right, normalize, new_wfns, rot_mat,
                    cutoff, trunc_type);
                return make_tuple(error, new_wfns, rot_mat);
            },
            py::arg("dm"), py::arg("wfns"), py::arg("k"),
            py::arg("trace_right"), py::arg("normalize"), py::arg("cutoff"),
            py::arg("trunc_type") = TruncationTypes::Physical)
        .def_static("propagate_multi_wfn", &MovingEnvironment<S>::propagate_wfn,
                    py::arg("i"), py::arg("n_sites"), py::arg("mps"),
                    py::arg("forward"), py::arg("cg"));

    py::bind_vector<vector<shared_ptr<MovingEnvironment<S>>>>(
        m, "VectorMovingEnvironment");
}

template <typename S> void bind_hamiltonian(py::module &m) {
    py::class_<Hamiltonian<S>, shared_ptr<Hamiltonian<S>>>(m, "Hamiltonian")
        .def(py::init<S, int, const vector<uint8_t> &>())
        .def_readwrite("n_syms", &Hamiltonian<S>::n_syms)
        .def_readwrite("opf", &Hamiltonian<S>::opf)
        .def_readwrite("n_sites", &Hamiltonian<S>::n_sites)
        .def_readwrite("orb_sym", &Hamiltonian<S>::orb_sym)
        .def_readwrite("vacuum", &Hamiltonian<S>::vacuum)
        .def_readwrite("basis", &Hamiltonian<S>::basis)
        .def_readwrite("site_op_infos", &Hamiltonian<S>::site_op_infos)
        .def_readwrite("delayed", &Hamiltonian<S>::delayed)
        .def("get_site_ops", &Hamiltonian<S>::get_site_ops)
        .def("filter_site_ops", &Hamiltonian<S>::filter_site_ops)
        .def("find_site_op_info", &Hamiltonian<S>::find_site_op_info)
        .def("deallocate", &Hamiltonian<S>::deallocate);

    py::class_<HamiltonianQC<S>, shared_ptr<HamiltonianQC<S>>, Hamiltonian<S>>(
        m, "HamiltonianQC")
        .def(py::init<S, int, const vector<uint8_t> &,
                      const shared_ptr<FCIDUMP> &>())
        .def_readwrite("fcidump", &HamiltonianQC<S>::fcidump)
        .def_readwrite("mu", &HamiltonianQC<S>::mu)
        .def_readwrite("op_prims", &HamiltonianQC<S>::op_prims)
        .def("v", &HamiltonianQC<S>::v)
        .def("t", &HamiltonianQC<S>::t)
        .def("e", &HamiltonianQC<S>::e)
        .def("init_site_ops", &HamiltonianQC<S>::init_site_ops)
        .def("get_site_ops", &HamiltonianQC<S>::get_site_ops);
}

template <typename S, typename FL>
void bind_expect(py::module &m, const string &name) {

    py::class_<typename Expect<S, FL>::Iteration,
               shared_ptr<typename Expect<S, FL>::Iteration>>(
        m, (name + "Iteration").c_str())
        .def(py::init<const vector<pair<shared_ptr<OpExpr<S>>, FL>> &, double,
                      double, size_t, double>())
        .def(py::init<const vector<pair<shared_ptr<OpExpr<S>>, FL>> &, double,
                      double>())
        .def_readwrite("bra_error", &Expect<S, FL>::Iteration::bra_error)
        .def_readwrite("ket_error", &Expect<S, FL>::Iteration::ket_error)
        .def_readwrite("tmult", &Expect<S, FL>::Iteration::tmult)
        .def_readwrite("nflop", &Expect<S, FL>::Iteration::nflop)
        .def("__repr__", [](typename Expect<S, FL>::Iteration *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });

    py::class_<Expect<S, FL>, shared_ptr<Expect<S, FL>>>(m, name.c_str())
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &, ubond_t,
                      ubond_t>())
        .def(
            py::init<const shared_ptr<MovingEnvironment<S>> &, ubond_t, ubond_t,
                     double, const vector<double> &, const vector<int> &>())
        .def_readwrite("iprint", &Expect<S, FL>::iprint)
        .def_readwrite("cutoff", &Expect<S, FL>::cutoff)
        .def_readwrite("beta", &Expect<S, FL>::beta)
        .def_readwrite("partition_weights", &Expect<S, FL>::partition_weights)
        .def_readwrite("me", &Expect<S, FL>::me)
        .def_readwrite("bra_bond_dim", &Expect<S, FL>::bra_bond_dim)
        .def_readwrite("ket_bond_dim", &Expect<S, FL>::ket_bond_dim)
        .def_readwrite("expectations", &Expect<S, FL>::expectations)
        .def_readwrite("forward", &Expect<S, FL>::forward)
        .def_readwrite("trunc_type", &Expect<S, FL>::trunc_type)
        .def_readwrite("ex_type", &Expect<S, FL>::ex_type)
        .def_readwrite("algo_type", &Expect<S, FL>::algo_type)
        .def("update_one_dot", &Expect<S, FL>::update_one_dot)
        .def("update_multi_one_dot", &Expect<S, FL>::update_multi_one_dot)
        .def("update_two_dot", &Expect<S, FL>::update_two_dot)
        .def("update_multi_two_dot", &Expect<S, FL>::update_multi_two_dot)
        .def("blocking", &Expect<S, FL>::blocking)
        .def("sweep", &Expect<S, FL>::sweep)
        .def("solve", &Expect<S, FL>::solve, py::arg("propagate"),
             py::arg("forward") = true)
        .def("get_1pdm_spatial", &Expect<S, FL>::get_1pdm_spatial,
             py::arg("n_physical_sites") = (uint16_t)0U)
        .def("get_1pdm", &Expect<S, FL>::get_1pdm,
             py::arg("n_physical_sites") = (uint16_t)0U)
        .def("get_2pdm_spatial", &Expect<S, FL>::get_2pdm_spatial,
             py::arg("n_physical_sites") = (uint16_t)0U)
        .def("get_2pdm", &Expect<S, FL>::get_2pdm,
             py::arg("n_physical_sites") = (uint16_t)0U)
        .def("get_1npc_spatial", &Expect<S, FL>::get_1npc_spatial, py::arg("s"),
             py::arg("n_physical_sites") = (uint16_t)0U)
        .def("get_1npc", &Expect<S, FL>::get_1npc, py::arg("s"),
             py::arg("n_physical_sites") = (uint16_t)0U);
}

template <typename S> void bind_algorithms(py::module &m) {

    py::class_<typename DMRG<S>::Iteration,
               shared_ptr<typename DMRG<S>::Iteration>>(m, "DMRGIteration")
        .def(py::init<const vector<double> &, double, int, int, size_t,
                      double>())
        .def(py::init<const vector<double> &, double, int, int>())
        .def_readwrite("mmps", &DMRG<S>::Iteration::mmps)
        .def_readwrite("energies", &DMRG<S>::Iteration::energies)
        .def_readwrite("error", &DMRG<S>::Iteration::error)
        .def_readwrite("ndav", &DMRG<S>::Iteration::ndav)
        .def_readwrite("tdav", &DMRG<S>::Iteration::tdav)
        .def_readwrite("nflop", &DMRG<S>::Iteration::nflop)
        .def("__repr__", [](typename DMRG<S>::Iteration *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });

    py::class_<DMRG<S>, shared_ptr<DMRG<S>>>(m, "DMRG")
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &,
                      const vector<ubond_t> &, const vector<double> &>())
        .def_readwrite("iprint", &DMRG<S>::iprint)
        .def_readwrite("cutoff", &DMRG<S>::cutoff)
        .def_readwrite("quanta_cutoff", &DMRG<S>::quanta_cutoff)
        .def_readwrite("me", &DMRG<S>::me)
        .def_readwrite("ext_mes", &DMRG<S>::ext_mes)
        .def_readwrite("ext_mpss", &DMRG<S>::ext_mpss)
        .def_readwrite("state_specific", &DMRG<S>::state_specific)
        .def_readwrite("bond_dims", &DMRG<S>::bond_dims)
        .def_readwrite("noises", &DMRG<S>::noises)
        .def_readwrite("davidson_conv_thrds", &DMRG<S>::davidson_conv_thrds)
        .def_readwrite("davidson_max_iter", &DMRG<S>::davidson_max_iter)
        .def_readwrite("davidson_soft_max_iter",
                       &DMRG<S>::davidson_soft_max_iter)
        .def_readwrite("davidson_shift", &DMRG<S>::davidson_shift)
        .def_readwrite("davidson_type", &DMRG<S>::davidson_type)
        .def_readwrite("conn_adjust_step", &DMRG<S>::conn_adjust_step)
        .def_readwrite("energies", &DMRG<S>::energies)
        .def_readwrite("discarded_weights", &DMRG<S>::discarded_weights)
        .def_readwrite("mps_quanta", &DMRG<S>::mps_quanta)
        .def_readwrite("sweep_energies", &DMRG<S>::sweep_energies)
        .def_readwrite("sweep_discarded_weights",
                       &DMRG<S>::sweep_discarded_weights)
        .def_readwrite("sweep_quanta", &DMRG<S>::sweep_quanta)
        .def_readwrite("forward", &DMRG<S>::forward)
        .def_readwrite("noise_type", &DMRG<S>::noise_type)
        .def_readwrite("trunc_type", &DMRG<S>::trunc_type)
        .def_readwrite("decomp_type", &DMRG<S>::decomp_type)
        .def_readwrite("decomp_last_site", &DMRG<S>::decomp_last_site)
        .def_readwrite("sweep_cumulative_nflop",
                       &DMRG<S>::sweep_cumulative_nflop)
        .def_readwrite("sweep_max_pket_size", &DMRG<S>::sweep_max_pket_size)
        .def_readwrite("sweep_max_eff_ham_size",
                       &DMRG<S>::sweep_max_eff_ham_size)
        .def("update_two_dot", &DMRG<S>::update_two_dot)
        .def("update_one_dot", &DMRG<S>::update_one_dot)
        .def("update_multi_two_dot", &DMRG<S>::update_multi_two_dot)
        .def("update_multi_one_dot", &DMRG<S>::update_multi_one_dot)
        .def("blocking", &DMRG<S>::blocking)
        .def("partial_sweep", &DMRG<S>::partial_sweep)
        .def("connection_sweep", &DMRG<S>::connection_sweep)
        .def("unordered_sweep", &DMRG<S>::unordered_sweep)
        .def("sweep", &DMRG<S>::sweep)
        .def("solve", &DMRG<S>::solve, py::arg("n_sweeps"),
             py::arg("forward") = true, py::arg("tol") = 1E-6);

    py::class_<typename TDDMRG<S>::Iteration,
               shared_ptr<typename TDDMRG<S>::Iteration>>(m, "TDDMRGIteration")
        .def(py::init<double, double, double, int, int, size_t, double>())
        .def(py::init<double, double, double, int, int>())
        .def_readwrite("mmps", &TDDMRG<S>::Iteration::mmps)
        .def_readwrite("energy", &TDDMRG<S>::Iteration::energy)
        .def_readwrite("normsq", &TDDMRG<S>::Iteration::normsq)
        .def_readwrite("error", &TDDMRG<S>::Iteration::error)
        .def_readwrite("nmult", &TDDMRG<S>::Iteration::nmult)
        .def_readwrite("tmult", &TDDMRG<S>::Iteration::tmult)
        .def_readwrite("nflop", &TDDMRG<S>::Iteration::nflop)
        .def("__repr__", [](typename TDDMRG<S>::Iteration *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });

    py::class_<TDDMRG<S>, shared_ptr<TDDMRG<S>>>(m, "TDDMRG")
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &,
                      const vector<ubond_t> &, const vector<double> &>())
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &,
                      const vector<ubond_t> &>())
        .def_readwrite("me", &TDDMRG<S>::me)
        .def_readwrite("lme", &TDDMRG<S>::lme)
        .def_readwrite("rme", &TDDMRG<S>::rme)
        .def_readwrite("iprint", &TDDMRG<S>::iprint)
        .def_readwrite("cutoff", &TDDMRG<S>::cutoff)
        .def_readwrite("bond_dims", &TDDMRG<S>::bond_dims)
        .def_readwrite("noises", &TDDMRG<S>::noises)
        .def_readwrite("energies", &TDDMRG<S>::energies)
        .def_readwrite("normsqs", &TDDMRG<S>::normsqs)
        .def_readwrite("discarded_weights", &TDDMRG<S>::discarded_weights)
        .def_readwrite("forward", &TDDMRG<S>::forward)
        .def_readwrite("n_sub_sweeps", &TDDMRG<S>::n_sub_sweeps)
        .def_readwrite("weights", &TDDMRG<S>::weights)
        .def_readwrite("mode", &TDDMRG<S>::mode)
        .def_readwrite("noise_type", &TDDMRG<S>::noise_type)
        .def_readwrite("trunc_type", &TDDMRG<S>::trunc_type)
        .def_readwrite("decomp_type", &TDDMRG<S>::decomp_type)
        .def_readwrite("decomp_last_site", &TDDMRG<S>::decomp_last_site)
        .def_readwrite("hermitian", &TDDMRG<S>::hermitian)
        .def_readwrite("sweep_cumulative_nflop",
                       &TDDMRG<S>::sweep_cumulative_nflop)
        .def("update_one_dot", &TDDMRG<S>::update_one_dot)
        .def("update_two_dot", &TDDMRG<S>::update_two_dot)
        .def("blocking", &TDDMRG<S>::blocking)
        .def("sweep", &TDDMRG<S>::sweep)
        .def("normalize", &TDDMRG<S>::normalize)
        .def("solve", &TDDMRG<S>::solve, py::arg("n_sweeps"), py::arg("beta"),
             py::arg("forward") = true, py::arg("tol") = 1E-6);

    py::class_<typename TimeEvolution<S>::Iteration,
               shared_ptr<typename TimeEvolution<S>::Iteration>>(
        m, "TimeEvolutionIteration")
        .def(py::init<double, double, double, int, int, int, size_t, double>())
        .def(py::init<double, double, double, int, int, int>())
        .def_readwrite("mmps", &TimeEvolution<S>::Iteration::mmps)
        .def_readwrite("energy", &TimeEvolution<S>::Iteration::energy)
        .def_readwrite("normsq", &TimeEvolution<S>::Iteration::normsq)
        .def_readwrite("error", &TimeEvolution<S>::Iteration::error)
        .def_readwrite("nexpo", &TimeEvolution<S>::Iteration::nexpo)
        .def_readwrite("nexpok", &TimeEvolution<S>::Iteration::nexpok)
        .def_readwrite("texpo", &TimeEvolution<S>::Iteration::texpo)
        .def_readwrite("nflop", &TimeEvolution<S>::Iteration::nflop)
        .def("__repr__", [](typename TimeEvolution<S>::Iteration *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });

    py::class_<TimeEvolution<S>, shared_ptr<TimeEvolution<S>>>(m,
                                                               "TimeEvolution")
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &,
                      const vector<ubond_t> &, TETypes>())
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &,
                      const vector<ubond_t> &, TETypes, int>())
        .def_readwrite("iprint", &TimeEvolution<S>::iprint)
        .def_readwrite("cutoff", &TimeEvolution<S>::cutoff)
        .def_readwrite("me", &TimeEvolution<S>::me)
        .def_readwrite("bond_dims", &TimeEvolution<S>::bond_dims)
        .def_readwrite("noises", &TimeEvolution<S>::noises)
        .def_readwrite("energies", &TimeEvolution<S>::energies)
        .def_readwrite("normsqs", &TimeEvolution<S>::normsqs)
        .def_readwrite("discarded_weights",
                       &TimeEvolution<S>::discarded_weights)
        .def_readwrite("forward", &TimeEvolution<S>::forward)
        .def_readwrite("n_sub_sweeps", &TimeEvolution<S>::n_sub_sweeps)
        .def_readwrite("weights", &TimeEvolution<S>::weights)
        .def_readwrite("mode", &TimeEvolution<S>::mode)
        .def_readwrite("noise_type", &TimeEvolution<S>::noise_type)
        .def_readwrite("trunc_type", &TimeEvolution<S>::trunc_type)
        .def_readwrite("trunc_pattern", &TimeEvolution<S>::trunc_pattern)
        .def_readwrite("decomp_type", &TimeEvolution<S>::decomp_type)
        .def_readwrite("normalize_mps", &TimeEvolution<S>::normalize_mps)
        .def_readwrite("hermitian", &TimeEvolution<S>::hermitian)
        .def_readwrite("sweep_cumulative_nflop",
                       &TimeEvolution<S>::sweep_cumulative_nflop)
        .def("update_one_dot", &TimeEvolution<S>::update_one_dot)
        .def("update_two_dot", &TimeEvolution<S>::update_two_dot)
        .def("update_multi_one_dot", &TimeEvolution<S>::update_multi_one_dot)
        .def("update_multi_two_dot", &TimeEvolution<S>::update_multi_two_dot)
        .def("blocking", &TimeEvolution<S>::blocking)
        .def("sweep", &TimeEvolution<S>::sweep)
        .def("normalize", &TimeEvolution<S>::normalize)
        .def("solve", &TimeEvolution<S>::solve, py::arg("n_sweeps"),
             py::arg("beta"), py::arg("forward") = true, py::arg("tol") = 1E-6);

    py::class_<typename Linear<S>::Iteration,
               shared_ptr<typename Linear<S>::Iteration>>(m, "LinearIteration")
        .def(py::init<const vector<double> &, double, int, int, int, size_t,
                      double>())
        .def(py::init<const vector<double> &, double, int, int, int>())
        .def_readwrite("mmps", &Linear<S>::Iteration::mmps)
        .def_readwrite("targets", &Linear<S>::Iteration::targets)
        .def_readwrite("error", &Linear<S>::Iteration::error)
        .def_readwrite("nmult", &Linear<S>::Iteration::nmult)
        .def_readwrite("nmultp", &Linear<S>::Iteration::nmultp)
        .def_readwrite("tmult", &Linear<S>::Iteration::tmult)
        .def_readwrite("nflop", &Linear<S>::Iteration::nflop)
        .def("__repr__", [](typename Linear<S>::Iteration *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });

    py::class_<Linear<S>, shared_ptr<Linear<S>>>(m, "Linear")
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &,
                      const vector<ubond_t> &, const vector<ubond_t> &>())
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &,
                      const vector<ubond_t> &, const vector<ubond_t> &,
                      const vector<double> &>())
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &,
                      const shared_ptr<MovingEnvironment<S>> &,
                      const vector<ubond_t> &, const vector<ubond_t> &>())
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &,
                      const shared_ptr<MovingEnvironment<S>> &,
                      const vector<ubond_t> &, const vector<ubond_t> &,
                      const vector<double> &>())
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &,
                      const shared_ptr<MovingEnvironment<S>> &,
                      const shared_ptr<MovingEnvironment<S>> &,
                      const vector<ubond_t> &, const vector<ubond_t> &>())
        .def(py::init<const shared_ptr<MovingEnvironment<S>> &,
                      const shared_ptr<MovingEnvironment<S>> &,
                      const shared_ptr<MovingEnvironment<S>> &,
                      const vector<ubond_t> &, const vector<ubond_t> &,
                      const vector<double> &>())
        .def_readwrite("iprint", &Linear<S>::iprint)
        .def_readwrite("cutoff", &Linear<S>::cutoff)
        .def_readwrite("lme", &Linear<S>::lme)
        .def_readwrite("rme", &Linear<S>::rme)
        .def_readwrite("tme", &Linear<S>::tme)
        .def_readwrite("ext_tmes", &Linear<S>::ext_tmes)
        .def_readwrite("ext_mpss", &Linear<S>::ext_mpss)
        .def_readwrite("ext_targets", &Linear<S>::ext_targets)
        .def_readwrite("ext_target_at_site", &Linear<S>::ext_target_at_site)
        .def_readwrite("bra_bond_dims", &Linear<S>::bra_bond_dims)
        .def_readwrite("ket_bond_dims", &Linear<S>::ket_bond_dims)
        .def_readwrite("target_bra_bond_dim", &Linear<S>::target_bra_bond_dim)
        .def_readwrite("target_ket_bond_dim", &Linear<S>::target_ket_bond_dim)
        .def_readwrite("noises", &Linear<S>::noises)
        .def_readwrite("targets", &Linear<S>::targets)
        .def_readwrite("discarded_weights", &Linear<S>::discarded_weights)
        .def_readwrite("sweep_targets", &Linear<S>::sweep_targets)
        .def_readwrite("sweep_discarded_weights",
                       &Linear<S>::sweep_discarded_weights)
        .def_readwrite("forward", &Linear<S>::forward)
        .def_readwrite("conv_type", &Linear<S>::conv_type)
        .def_readwrite("noise_type", &Linear<S>::noise_type)
        .def_readwrite("trunc_type", &Linear<S>::trunc_type)
        .def_readwrite("decomp_type", &Linear<S>::decomp_type)
        .def_readwrite("eq_type", &Linear<S>::eq_type)
        .def_readwrite("ex_type", &Linear<S>::ex_type)
        .def_readwrite("algo_type", &Linear<S>::algo_type)
        .def_readwrite("precondition_cg", &Linear<S>::precondition_cg)
        .def_readwrite("cg_n_harmonic_projection",
                       &Linear<S>::cg_n_harmonic_projection)
        .def_readwrite("gcrotmk_size", &Linear<S>::gcrotmk_size)
        .def_readwrite("decomp_last_site", &Linear<S>::decomp_last_site)
        .def_readwrite("sweep_cumulative_nflop",
                       &Linear<S>::sweep_cumulative_nflop)
        .def_readwrite("sweep_max_pket_size", &Linear<S>::sweep_max_pket_size)
        .def_readwrite("sweep_max_eff_ham_size",
                       &Linear<S>::sweep_max_eff_ham_size)
        .def_readwrite("minres_conv_thrds", &Linear<S>::minres_conv_thrds)
        .def_readwrite("minres_max_iter", &Linear<S>::minres_max_iter)
        .def_readwrite("minres_soft_max_iter", &Linear<S>::minres_soft_max_iter)
        .def_readwrite("conv_required_sweeps", &Linear<S>::conv_required_sweeps)
        .def_readwrite("gf_omega", &Linear<S>::gf_omega)
        .def_readwrite("gf_eta", &Linear<S>::gf_eta)
        .def_readwrite("gf_extra_omegas", &Linear<S>::gf_extra_omegas)
        .def_readwrite("gf_extra_targets", &Linear<S>::gf_extra_targets)
        .def_readwrite("gf_extra_omegas_at_site",
                       &Linear<S>::gf_extra_omegas_at_site)
        .def_readwrite("gf_extra_eta", &Linear<S>::gf_extra_eta)
        .def_readwrite("gf_extra_ext_targets", &Linear<S>::gf_extra_ext_targets)
        .def_readwrite("right_weight", &Linear<S>::right_weight)
        .def_readwrite("complex_weights", &Linear<S>::complex_weights)
        .def("update_one_dot", &Linear<S>::update_one_dot)
        .def("update_two_dot", &Linear<S>::update_two_dot)
        .def("blocking", &Linear<S>::blocking)
        .def("sweep", &Linear<S>::sweep)
        .def("solve", &Linear<S>::solve, py::arg("n_sweeps"),
             py::arg("forward") = true, py::arg("tol") = 1E-6);

    bind_expect<S, double>(m, "Expect");
    bind_expect<S, complex<double>>(m, "ComplexExpect");
}

template <typename S> void bind_parallel(py::module &m) {

    py::class_<ParallelCommunicator<S>, shared_ptr<ParallelCommunicator<S>>>(
        m, "ParallelCommunicator")
        .def(py::init<>())
        .def(py::init<int, int, int>())
        .def_readwrite("size", &ParallelCommunicator<S>::size)
        .def_readwrite("rank", &ParallelCommunicator<S>::rank)
        .def_readwrite("root", &ParallelCommunicator<S>::root)
        .def_readwrite("group", &ParallelCommunicator<S>::group)
        .def_readwrite("grank", &ParallelCommunicator<S>::grank)
        .def_readwrite("gsize", &ParallelCommunicator<S>::gsize)
        .def_readwrite("ngroup", &ParallelCommunicator<S>::ngroup)
        .def_readwrite("tcomm", &ParallelCommunicator<S>::tcomm)
        .def_readwrite("para_type", &ParallelCommunicator<S>::para_type)
        .def("get_parallel_type", &ParallelCommunicator<S>::get_parallel_type)
        .def("barrier", &ParallelCommunicator<S>::barrier)
        .def("split", &ParallelCommunicator<S>::split);

#ifdef _HAS_MPI
    py::class_<MPICommunicator<S>, shared_ptr<MPICommunicator<S>>,
               ParallelCommunicator<S>>(m, "MPICommunicator")
        .def(py::init<>())
        .def(py::init<int>());
#endif

    py::class_<ParallelRule<S>, shared_ptr<ParallelRule<S>>>(m, "ParallelRule")
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &>())
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &,
                      ParallelCommTypes>())
        .def_readwrite("comm", &ParallelRule<S>::comm)
        .def_readwrite("comm_type", &ParallelRule<S>::comm_type)
        .def("get_parallel_type", &ParallelRule<S>::get_parallel_type)
        .def("set_partition", &ParallelRule<S>::set_partition)
        .def("split", &ParallelRule<S>::split)
        .def("__call__", &ParallelRule<S>::operator())
        .def("is_root", &ParallelRule<S>::is_root)
        .def("available", &ParallelRule<S>::available)
        .def("own", &ParallelRule<S>::own)
        .def("owner", &ParallelRule<S>::owner)
        .def("repeat", &ParallelRule<S>::repeat)
        .def("partial", &ParallelRule<S>::partial);

    py::class_<ParallelRuleSumMPO<S>, shared_ptr<ParallelRuleSumMPO<S>>,
               ParallelRule<S>>(m, "ParallelRuleSumMPO")
        .def_readwrite("n_sites", &ParallelRuleSumMPO<S>::n_sites)
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &>())
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &,
                      ParallelCommTypes>())
        .def(
            "index_available",
            [](ParallelRuleSumMPO<S> *self, py::args &args) -> bool {
                if (args.size() == 0)
                    return self->index_available();
                else if (args.size() == 1)
                    return self->index_available((uint16_t)args[0].cast<int>());
                else if (args.size() == 2)
                    return self->index_available((uint16_t)args[0].cast<int>(),
                                                 (uint16_t)args[1].cast<int>());
                else if (args.size() == 4)
                    return self->index_available((uint16_t)args[0].cast<int>(),
                                                 (uint16_t)args[1].cast<int>(),
                                                 (uint16_t)args[2].cast<int>(),
                                                 (uint16_t)args[3].cast<int>());
                else {
                    assert(false);
                    return false;
                }
            });

    py::class_<SumMPORule<S>, shared_ptr<SumMPORule<S>>, Rule<S>>(m,
                                                                  "SumMPORule")
        .def_readwrite("prim_rule", &SumMPORule<S>::prim_rule)
        .def_readwrite("para_rule", &SumMPORule<S>::para_rule)
        .def(py::init<const shared_ptr<Rule<S>> &,
                      const shared_ptr<ParallelRuleSumMPO<S>> &>());

    py::class_<ParallelFCIDUMP<S>, shared_ptr<ParallelFCIDUMP<S>>, FCIDUMP>(
        m, "ParallelFCIDUMP")
        .def_readwrite("rule", &ParallelFCIDUMP<S>::rule)
        .def(py::init<const shared_ptr<ParallelRuleSumMPO<S>> &>());

    py::class_<ParallelRuleQC<S>, shared_ptr<ParallelRuleQC<S>>,
               ParallelRule<S>>(m, "ParallelRuleQC")
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &>())
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &,
                      ParallelCommTypes>());

    py::class_<ParallelRuleOneBodyQC<S>, shared_ptr<ParallelRuleOneBodyQC<S>>,
               ParallelRule<S>>(m, "ParallelRuleOneBodyQC")
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &>())
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &,
                      ParallelCommTypes>());

    py::class_<ParallelRuleNPDMQC<S>, shared_ptr<ParallelRuleNPDMQC<S>>,
               ParallelRule<S>>(m, "ParallelRuleNPDMQC")
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &>())
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &,
                      ParallelCommTypes>());

    py::class_<ParallelRulePDM1QC<S>, shared_ptr<ParallelRulePDM1QC<S>>,
               ParallelRule<S>>(m, "ParallelRulePDM1QC")
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &>())
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &,
                      ParallelCommTypes>());

    py::class_<ParallelRulePDM2QC<S>, shared_ptr<ParallelRulePDM2QC<S>>,
               ParallelRule<S>>(m, "ParallelRulePDM2QC")
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &>())
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &,
                      ParallelCommTypes>());

    py::class_<ParallelRuleSiteQC<S>, shared_ptr<ParallelRuleSiteQC<S>>,
               ParallelRule<S>>(m, "ParallelRuleSiteQC")
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &>())
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &,
                      ParallelCommTypes>());

    py::class_<ParallelRuleIdentity<S>, shared_ptr<ParallelRuleIdentity<S>>,
               ParallelRule<S>>(m, "ParallelRuleIdentity")
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &>())
        .def(py::init<const shared_ptr<ParallelCommunicator<S>> &,
                      ParallelCommTypes>());

    py::class_<ParallelTensorFunctions<S>,
               shared_ptr<ParallelTensorFunctions<S>>, TensorFunctions<S>>(
        m, "ParallelTensorFunctions")
        .def(py::init<const shared_ptr<OperatorFunctions<S>> &,
                      const shared_ptr<ParallelRule<S>> &>());

    py::class_<ClassicParallelMPO<S>, shared_ptr<ClassicParallelMPO<S>>,
               MPO<S>>(m, "ClassicParallelMPO")
        .def_readwrite("prim_mpo", &ClassicParallelMPO<S>::prim_mpo)
        .def_readwrite("rule", &ClassicParallelMPO<S>::rule)
        .def(py::init<const shared_ptr<MPO<S>> &,
                      const shared_ptr<ParallelRule<S>> &>());

    py::class_<ParallelMPO<S>, shared_ptr<ParallelMPO<S>>, MPO<S>>(
        m, "ParallelMPO")
        .def_readwrite("prim_mpo", &ParallelMPO<S>::prim_mpo)
        .def_readwrite("rule", &ParallelMPO<S>::rule)
        .def(py::init<int, const shared_ptr<ParallelRule<S>> &>())
        .def(py::init<const shared_ptr<MPO<S>> &,
                      const shared_ptr<ParallelRule<S>> &>());
}

template <typename S> void bind_mpo(py::module &m) {

    py::class_<MPOSchemer<S>, shared_ptr<MPOSchemer<S>>>(m, "MPOSchemer")
        .def_readwrite("left_trans_site", &MPOSchemer<S>::left_trans_site)
        .def_readwrite("right_trans_site", &MPOSchemer<S>::right_trans_site)
        .def_readwrite("left_new_operator_names",
                       &MPOSchemer<S>::left_new_operator_names)
        .def_readwrite("right_new_operator_names",
                       &MPOSchemer<S>::right_new_operator_names)
        .def_readwrite("left_new_operator_exprs",
                       &MPOSchemer<S>::left_new_operator_exprs)
        .def_readwrite("right_new_operator_exprs",
                       &MPOSchemer<S>::right_new_operator_exprs)
        .def(py::init<uint16_t, uint16_t>())
        .def("copy", &MPOSchemer<S>::copy)
        .def("get_transform_formulas", &MPOSchemer<S>::get_transform_formulas);

    py::class_<MPO<S>, shared_ptr<MPO<S>>>(m, "MPO")
        .def(py::init<int>())
        .def_readwrite("n_sites", &MPO<S>::n_sites)
        .def_readwrite("const_e", &MPO<S>::const_e)
        .def_readwrite("tensors", &MPO<S>::tensors)
        .def_readwrite("basis", &MPO<S>::basis)
        .def_readwrite("sparse_form", &MPO<S>::sparse_form)
        .def_readwrite("left_operator_names", &MPO<S>::left_operator_names)
        .def_readwrite("right_operator_names", &MPO<S>::right_operator_names)
        .def_readwrite("middle_operator_names", &MPO<S>::middle_operator_names)
        .def_readwrite("left_operator_exprs", &MPO<S>::left_operator_exprs)
        .def_readwrite("right_operator_exprs", &MPO<S>::right_operator_exprs)
        .def_readwrite("middle_operator_exprs", &MPO<S>::middle_operator_exprs)
        .def_readwrite("op", &MPO<S>::op)
        .def_readwrite("schemer", &MPO<S>::schemer)
        .def_readwrite("tf", &MPO<S>::tf)
        .def_readwrite("site_op_infos", &MPO<S>::site_op_infos)
        .def_readwrite("schemer", &MPO<S>::schemer)
        .def_readwrite("archive_marks", &MPO<S>::archive_marks)
        .def_readwrite("archive_schemer_mark", &MPO<S>::archive_schemer_mark)
        .def_readwrite("archive_filename", &MPO<S>::archive_filename)
        .def("reduce_data", &MPO<S>::reduce_data)
        .def("load_data",
             (void (MPO<S>::*)(const string &, bool)) & MPO<S>::load_data,
             py::arg("filename"), py::arg("minimal") = false)
        .def("save_data",
             (void (MPO<S>::*)(const string &) const) & MPO<S>::save_data)
        .def("get_blocking_formulas", &MPO<S>::get_blocking_formulas)
        .def("get_ancilla_type", &MPO<S>::get_ancilla_type)
        .def("get_parallel_type", &MPO<S>::get_parallel_type)
        .def("estimate_storage", &MPO<S>::estimate_storage, py::arg("info"),
             py::arg("dot"))
        .def("deallocate", &MPO<S>::deallocate)
        .def("deep_copy", &MPO<S>::deep_copy)
        .def("__neg__",
             [](MPO<S> *self) { return -make_shared<MPO<S>>(*self); })
        .def("__mul__", [](MPO<S> *self,
                           double d) { return d * make_shared<MPO<S>>(*self); })
        .def("__rmul__", [](MPO<S> *self, double d) {
            return d * make_shared<MPO<S>>(*self);
        });

    py::class_<Rule<S>, shared_ptr<Rule<S>>>(m, "Rule")
        .def(py::init<>())
        .def("__call__", &Rule<S>::operator());

    py::class_<NoTransposeRule<S>, shared_ptr<NoTransposeRule<S>>, Rule<S>>(
        m, "NoTransposeRule")
        .def_readwrite("prim_rule", &NoTransposeRule<S>::prim_rule)
        .def(py::init<const shared_ptr<Rule<S>> &>());

    py::class_<AntiHermitianRuleQC<S>, shared_ptr<AntiHermitianRuleQC<S>>,
               Rule<S>>(m, "AntiHermitianRuleQC")
        .def_readwrite("prim_rule", &AntiHermitianRuleQC<S>::prim_rule)
        .def(py::init<const shared_ptr<Rule<S>> &>());

    py::class_<RuleQC<S>, shared_ptr<RuleQC<S>>, Rule<S>>(m, "RuleQC")
        .def(py::init<>())
        .def(py::init<bool, bool, bool, bool, bool, bool>());

    py::class_<SimplifiedMPO<S>, shared_ptr<SimplifiedMPO<S>>, MPO<S>>(
        m, "SimplifiedMPO")
        .def_readwrite("prim_mpo", &SimplifiedMPO<S>::prim_mpo)
        .def_readwrite("rule", &SimplifiedMPO<S>::rule)
        .def_readwrite("collect_terms", &SimplifiedMPO<S>::collect_terms)
        .def_readwrite("use_intermediate", &SimplifiedMPO<S>::use_intermediate)
        .def_readwrite("intermediate_ops", &SimplifiedMPO<S>::intermediate_ops)
        .def(
            py::init<const shared_ptr<MPO<S>> &, const shared_ptr<Rule<S>> &>())
        .def(py::init<const shared_ptr<MPO<S>> &, const shared_ptr<Rule<S>> &,
                      bool>())
        .def(py::init<const shared_ptr<MPO<S>> &, const shared_ptr<Rule<S>> &,
                      bool, bool>())
        .def(py::init<const shared_ptr<MPO<S>> &, const shared_ptr<Rule<S>> &,
                      bool, bool, OpNamesSet>())
        .def("simplify_expr", &SimplifiedMPO<S>::simplify_expr)
        .def("simplify_symbolic", &SimplifiedMPO<S>::simplify_symbolic)
        .def("simplify", &SimplifiedMPO<S>::simplify);

    py::class_<FusedMPO<S>, shared_ptr<FusedMPO<S>>, MPO<S>>(m, "FusedMPO")
        .def(py::init<const shared_ptr<MPO<S>> &,
                      const vector<shared_ptr<StateInfo<S>>> &, uint16_t,
                      uint16_t>())
        .def(py::init<const shared_ptr<MPO<S>> &,
                      const vector<shared_ptr<StateInfo<S>>> &, uint16_t,
                      uint16_t, const shared_ptr<StateInfo<S>> &>());

    py::class_<IdentityMPO<S>, shared_ptr<IdentityMPO<S>>, MPO<S>>(
        m, "IdentityMPO")
        .def(py::init<const vector<shared_ptr<StateInfo<S>>> &,
                      const vector<shared_ptr<StateInfo<S>>> &, S,
                      const shared_ptr<OperatorFunctions<S>> &>())
        .def(py::init<const vector<shared_ptr<StateInfo<S>>> &,
                      const vector<shared_ptr<StateInfo<S>>> &, S, S,
                      const shared_ptr<OperatorFunctions<S>> &>())
        .def(py::init<const vector<shared_ptr<StateInfo<S>>> &,
                      const vector<shared_ptr<StateInfo<S>>> &, S, S,
                      const shared_ptr<OperatorFunctions<S>> &,
                      const vector<uint8_t> &, const vector<uint8_t> &>())
        .def(py::init<const Hamiltonian<S> &>());

    py::class_<SiteMPO<S>, shared_ptr<SiteMPO<S>>, MPO<S>>(m, "SiteMPO")
        .def(py::init<const Hamiltonian<S> &,
                      const shared_ptr<OpElement<S>> &>())
        .def(py::init<const Hamiltonian<S> &, const shared_ptr<OpElement<S>> &,
                      int>());

    py::class_<LocalMPO<S>, shared_ptr<LocalMPO<S>>, MPO<S>>(m, "LocalMPO")
        .def(py::init<const Hamiltonian<S> &,
                      const vector<shared_ptr<OpElement<S>>> &>());

    py::class_<MPOQC<S>, shared_ptr<MPOQC<S>>, MPO<S>>(m, "MPOQC")
        .def_readwrite("mode", &MPOQC<S>::mode)
        .def(py::init<const HamiltonianQC<S> &>())
        .def(py::init<const HamiltonianQC<S> &, QCTypes>())
        .def(py::init<const HamiltonianQC<S> &, QCTypes, int>());

    py::class_<PDM1MPOQC<S>, shared_ptr<PDM1MPOQC<S>>, MPO<S>>(m, "PDM1MPOQC")
        .def(py::init<const Hamiltonian<S> &>())
        .def(py::init<const Hamiltonian<S> &, uint8_t>())
        .def("get_matrix", &PDM1MPOQC<S>::template get_matrix<double>)
        .def("get_matrix", &PDM1MPOQC<S>::template get_matrix<complex<double>>)
        .def("get_matrix_spatial",
             &PDM1MPOQC<S>::template get_matrix_spatial<double>)
        .def("get_matrix_spatial",
             &PDM1MPOQC<S>::template get_matrix_spatial<complex<double>>);

    py::class_<NPC1MPOQC<S>, shared_ptr<NPC1MPOQC<S>>, MPO<S>>(m, "NPC1MPOQC")
        .def(py::init<const Hamiltonian<S> &>());

    py::class_<AncillaMPO<S>, shared_ptr<AncillaMPO<S>>, MPO<S>>(m,
                                                                 "AncillaMPO")
        .def_readwrite("n_physical_sites", &AncillaMPO<S>::n_physical_sites)
        .def_readwrite("prim_mpo", &AncillaMPO<S>::prim_mpo)
        .def(py::init<const shared_ptr<MPO<S>> &>())
        .def(py::init<const shared_ptr<MPO<S>> &, bool>());

    py::class_<ArchivedMPO<S>, shared_ptr<ArchivedMPO<S>>, MPO<S>>(
        m, "ArchivedMPO")
        .def(py::init<const shared_ptr<MPO<S>> &>())
        .def(py::init<const shared_ptr<MPO<S>> &, const string &>());

    py::class_<DiagonalMPO<S>, shared_ptr<DiagonalMPO<S>>, MPO<S>>(
        m, "DiagonalMPO")
        .def(py::init<const shared_ptr<MPO<S>> &>())
        .def(py::init<const shared_ptr<MPO<S>> &,
                      const shared_ptr<Rule<S>> &>());

    py::class_<IdentityAddedMPO<S>, shared_ptr<IdentityAddedMPO<S>>, MPO<S>>(
        m, "IdentityAddedMPO")
        .def(py::init<const shared_ptr<MPO<S>> &>());
}

template <typename S> void bind_class(py::module &m, const string &name) {

    bind_expr<S>(m);
    bind_state_info<S>(m, name);
    bind_sparse<S>(m);
    bind_mps<S>(m);
    bind_cg<S>(m);
    bind_operator<S>(m);
    bind_partition<S>(m);
    bind_hamiltonian<S>(m);
    bind_algorithms<S>(m);
    bind_mpo<S>(m);
    bind_parallel<S>(m);
    bind_spin_specific<S>(m);
}

template <typename S, typename T>
void bind_trans(py::module &m, const string &aux_name) {

    m.def(("trans_state_info_to_" + aux_name).c_str(),
          &TransStateInfo<S, T>::forward);
    m.def(("trans_mps_info_to_" + aux_name).c_str(),
          &TransMPSInfo<S, T>::forward);
}

template <typename S, typename T>
auto bind_trans_spin_specific(py::module &m, const string &aux_name)
    -> decltype(typename S::is_su2_t(typename T::is_sz_t())) {

    m.def(("trans_connection_state_info_to_" + aux_name).c_str(),
          &TransStateInfo<T, S>::backward_connection);
    m.def(("trans_sparse_tensor_to_" + aux_name).c_str(),
          &TransSparseTensor<S, T>::forward);
    m.def(("trans_unfused_mps_to_" + aux_name).c_str(),
          &TransUnfusedMPS<S, T>::forward);
}

template <typename S = void> void bind_data(py::module &m) {

    py::bind_vector<vector<int>>(m, "VectorInt");
    py::bind_vector<vector<char>>(m, "VectorChar");
    py::bind_vector<vector<long long int>>(m, "VectorLLInt");
    py::bind_vector<vector<pair<int, int>>>(m, "VectorPIntInt");
    py::bind_vector<vector<pair<long long int, int>>>(m, "VectorPLLIntInt");
    py::bind_vector<vector<uint16_t>>(m, "VectorUInt16");
    py::bind_vector<vector<uint32_t>>(m, "VectorUInt32");
    py::bind_vector<vector<double>>(m, "VectorDouble");
    py::bind_vector<vector<long double>>(m, "VectorLDouble");
    py::bind_vector<vector<complex<double>>>(m, "VectorComplexDouble");
    py::bind_vector<vector<size_t>>(m, "VectorULInt");
    py::bind_vector<vector<vector<uint32_t>>>(m, "VectorVectorUInt32");
    py::bind_vector<vector<vector<double>>>(m, "VectorVectorDouble");
    py::bind_vector<vector<vector<int>>>(m, "VectorVectorInt");
    py::bind_vector<vector<vector<vector<double>>>>(m,
                                                    "VectorVectorVectorDouble");
    py::bind_vector<vector<uint8_t>>(m, "VectorUInt8")
        .def_property_readonly(
            "ptr",
            [](vector<uint8_t> *self) -> uint8_t * { return &(*self)[0]; })
        .def("__str__", [](vector<uint8_t> *self) {
            stringstream ss;
            ss << "VectorUInt8[ ";
            for (auto p : *self)
                ss << (int)p << " ";
            ss << "]";
            return ss.str();
        });

    py::class_<array<int, 4>>(m, "Array4Int")
        .def("__setitem__",
             [](array<int, 4> *self, size_t i, int t) { (*self)[i] = t; })
        .def("__getitem__",
             [](array<int, 4> *self, size_t i) { return (*self)[i]; })
        .def("__len__", [](array<int, 4> *self) { return self->size(); })
        .def("__repr__",
             [](array<int, 4> *self) {
                 stringstream ss;
                 ss << "(LEN=" << self->size() << ")[";
                 for (auto x : *self)
                     ss << x << ",";
                 ss << "]";
                 return ss.str();
             })
        .def("__iter__", [](array<int, 4> *self) {
            return py::make_iterator<
                py::return_value_policy::reference_internal, int *, int *,
                int &>(&(*self)[0], &(*self)[0] + self->size());
        });

    py::bind_vector<vector<array<int, 4>>>(m, "VectorArray4Int");

    bind_array<uint8_t>(m, "ArrayUInt8")
        .def("__str__", [](Array<uint8_t> *self) {
            stringstream ss;
            ss << "ArrayUInt8(LEN=" << self->n << ")[ ";
            for (size_t i = 0; i < self->n; i++)
                ss << (int)self->data[i] << " ";
            ss << "]";
            return ss.str();
        });

    bind_array<uint16_t>(m, "ArrayUInt16");
    bind_array<uint32_t>(m, "ArrayUInt32");

    if (sizeof(ubond_t) == sizeof(uint8_t)) {
        m.attr("VectorUBond") = m.attr("VectorUInt8");
        m.attr("ArrayUBond") = m.attr("ArrayUInt8");
    } else if (sizeof(ubond_t) == sizeof(uint16_t)) {
        m.attr("VectorUBond") = m.attr("VectorUInt16");
        m.attr("ArrayUBond") = m.attr("ArrayUInt16");
    } else if (sizeof(ubond_t) == sizeof(uint32_t)) {
        m.attr("VectorUBond") = m.attr("VectorUInt32");
        m.attr("ArrayUBond") = m.attr("ArrayUInt32");
    }

    if (sizeof(MKL_INT) == sizeof(int))
        m.attr("VectorMKLInt") = m.attr("VectorInt");
    else if (sizeof(MKL_INT) == sizeof(long long int))
        m.attr("VectorMKLInt") = m.attr("VectorLLInt");

    py::bind_map<map<string, string>>(m, "MapStrStr");
}

template <typename S = void> void bind_types(py::module &m) {

    py::class_<PointGroup, shared_ptr<PointGroup>>(m, "PointGroup")
        .def_static("swap_c1", &PointGroup::swap_c1)
        .def_static("swap_ci", &PointGroup::swap_ci)
        .def_static("swap_cs", &PointGroup::swap_cs)
        .def_static("swap_c2", &PointGroup::swap_c2)
        .def_static("swap_c2h", &PointGroup::swap_c2h)
        .def_static("swap_c2v", &PointGroup::swap_c2v)
        .def_static("swap_d2", &PointGroup::swap_d2)
        .def_static("swap_d2h", &PointGroup::swap_d2h);

    py::enum_<OpNames>(m, "OpNames", py::arithmetic())
        .value("H", OpNames::H)
        .value("I", OpNames::I)
        .value("N", OpNames::N)
        .value("NN", OpNames::NN)
        .value("C", OpNames::C)
        .value("D", OpNames::D)
        .value("R", OpNames::R)
        .value("RD", OpNames::RD)
        .value("A", OpNames::A)
        .value("AD", OpNames::AD)
        .value("P", OpNames::P)
        .value("PD", OpNames::PD)
        .value("B", OpNames::B)
        .value("BD", OpNames::BD)
        .value("Q", OpNames::Q)
        .value("TR", OpNames::TR)
        .value("TS", OpNames::TS)
        .value("Zero", OpNames::Zero)
        .value("PDM1", OpNames::PDM1)
        .value("PDM2", OpNames::PDM2)
        .value("CCDD", OpNames::CCDD)
        .value("CCD", OpNames::CCD)
        .value("CDC", OpNames::CDC)
        .value("CDD", OpNames::CDD)
        .value("DCC", OpNames::DCC)
        .value("DCD", OpNames::DCD)
        .value("DDC", OpNames::DDC)
        .value("TEMP", OpNames::TEMP);

    py::enum_<DelayedOpNames>(m, "DelayedOpNames", py::arithmetic())
        .value("Nothing", DelayedOpNames::None)
        .value("H", DelayedOpNames::H)
        .value("Normal", DelayedOpNames::Normal)
        .value("R", DelayedOpNames::R)
        .value("RD", DelayedOpNames::RD)
        .value("P", DelayedOpNames::P)
        .value("PD", DelayedOpNames::PD)
        .value("Q", DelayedOpNames::Q)
        .value("CCDD", DelayedOpNames::CCDD)
        .value("CCD", DelayedOpNames::CCD)
        .value("CDD", DelayedOpNames::CDD)
        .value("TR", DelayedOpNames::TR)
        .value("TS", DelayedOpNames::TS)
        .def(py::self & py::self)
        .def(py::self | py::self);

    py::enum_<OpTypes>(m, "OpTypes", py::arithmetic())
        .value("Zero", OpTypes::Zero)
        .value("Elem", OpTypes::Elem)
        .value("Prod", OpTypes::Prod)
        .value("Sum", OpTypes::Sum)
        .value("ElemRef", OpTypes::ElemRef)
        .value("SumProd", OpTypes::SumProd);

    py::enum_<NoiseTypes>(m, "NoiseTypes", py::arithmetic())
        .value("Nothing", NoiseTypes::None)
        .value("Wavefunction", NoiseTypes::Wavefunction)
        .value("DensityMatrix", NoiseTypes::DensityMatrix)
        .value("Perturbative", NoiseTypes::Perturbative)
        .value("Collected", NoiseTypes::Collected)
        .value("Reduced", NoiseTypes::Reduced)
        .value("Unscaled", NoiseTypes::Unscaled)
        .value("LowMem", NoiseTypes::LowMem)
        .value("ReducedPerturbative", NoiseTypes::ReducedPerturbative)
        .value("ReducedPerturbativeUnscaled",
               NoiseTypes::ReducedPerturbativeUnscaled)
        .value("PerturbativeUnscaled", NoiseTypes::PerturbativeUnscaled)
        .value("PerturbativeCollected", NoiseTypes::PerturbativeCollected)
        .value("PerturbativeUnscaledCollected",
               NoiseTypes::PerturbativeUnscaledCollected)
        .value("ReducedPerturbativeCollected",
               NoiseTypes::ReducedPerturbativeCollected)
        .value("ReducedPerturbativeUnscaledCollected",
               NoiseTypes::ReducedPerturbativeUnscaledCollected)
        .value("ReducedPerturbativeLowMem",
               NoiseTypes::ReducedPerturbativeLowMem)
        .value("ReducedPerturbativeUnscaledLowMem",
               NoiseTypes::ReducedPerturbativeUnscaledLowMem)
        .value("ReducedPerturbativeCollectedLowMem",
               NoiseTypes::ReducedPerturbativeCollectedLowMem)
        .value("ReducedPerturbativeUnscaledCollectedLowMem",
               NoiseTypes::ReducedPerturbativeUnscaledCollectedLowMem)
        .def(py::self & py::self)
        .def(py::self | py::self);

    py::enum_<TruncationTypes>(m, "TruncationTypes", py::arithmetic())
        .value("Physical", TruncationTypes::Physical)
        .value("Reduced", TruncationTypes::Reduced)
        .value("ReducedInversed", TruncationTypes::ReducedInversed)
        .value("KeepOne", TruncationTypes::KeepOne)
        .def(py::self * int(), "For KeepOne: Keep X states per quantum number");

    py::enum_<DecompositionTypes>(m, "DecompositionTypes", py::arithmetic())
        .value("DensityMatrix", DecompositionTypes::DensityMatrix)
        .value("SVD", DecompositionTypes::SVD)
        .value("PureSVD", DecompositionTypes::PureSVD);

    py::enum_<SymTypes>(m, "SymTypes", py::arithmetic())
        .value("RVec", SymTypes::RVec)
        .value("CVec", SymTypes::CVec)
        .value("Mat", SymTypes::Mat);

    py::enum_<AncillaTypes>(m, "AncillaTypes", py::arithmetic())
        .value("Nothing", AncillaTypes::None)
        .value("Ancilla", AncillaTypes::Ancilla);

    py::enum_<MPSTypes>(m, "MPSTypes", py::arithmetic())
        .value("Nothing", MPSTypes::None)
        .value("MultiWfn", MPSTypes::MultiWfn)
        .value("MultiCenter", MPSTypes::MultiCenter)
        .def(py::self & py::self)
        .def(py::self | py::self)
        .def(py::self ^ py::self);

    py::enum_<ActiveTypes>(m, "ActiveTypes", py::arithmetic())
        .value("Empty", ActiveTypes::Empty)
        .value("Active", ActiveTypes::Active)
        .value("Frozen", ActiveTypes::Frozen);

    py::bind_vector<vector<ActiveTypes>>(m, "VectorActTypes");

    py::enum_<SeqTypes>(m, "SeqTypes", py::arithmetic())
        .value("Nothing", SeqTypes::None)
        .value("Simple", SeqTypes::Simple)
        .value("Auto", SeqTypes::Auto)
        .value("Tasked", SeqTypes::Tasked)
        .value("SimpleTasked", SeqTypes::SimpleTasked)
        .def(py::self & py::self)
        .def(py::self | py::self);

    py::enum_<FuseTypes>(m, "FuseTypes", py::arithmetic())
        .value("NoFuseL", FuseTypes::NoFuseL)
        .value("NoFuseR", FuseTypes::NoFuseR)
        .value("FuseL", FuseTypes::FuseL)
        .value("FuseR", FuseTypes::FuseR)
        .value("FuseLR", FuseTypes::FuseLR);

    py::enum_<DavidsonTypes>(m, "DavidsonTypes", py::arithmetic())
        .value("GreaterThan", DavidsonTypes::GreaterThan)
        .value("LessThan", DavidsonTypes::LessThan)
        .value("CloseTo", DavidsonTypes::CloseTo)
        .value("Harmonic", DavidsonTypes::Harmonic)
        .value("HarmonicGreaterThan", DavidsonTypes::HarmonicGreaterThan)
        .value("HarmonicLessThan", DavidsonTypes::HarmonicLessThan)
        .value("HarmonicCloseTo", DavidsonTypes::HarmonicCloseTo)
        .value("DavidsonPrecond", DavidsonTypes::DavidsonPrecond)
        .value("NoPrecond", DavidsonTypes::NoPrecond)
        .value("Normal", DavidsonTypes::Normal)
        .def(py::self & py::self)
        .def(py::self | py::self);

    py::enum_<ExpectationAlgorithmTypes>(m, "ExpectationAlgorithmTypes",
                                         py::arithmetic())
        .value("Automatic", ExpectationAlgorithmTypes::Automatic)
        .value("Normal", ExpectationAlgorithmTypes::Normal)
        .value("Fast", ExpectationAlgorithmTypes::Fast);

    py::enum_<ExpectationTypes>(m, "ExpectationTypes", py::arithmetic())
        .value("Real", ExpectationTypes::Real)
        .value("Complex", ExpectationTypes::Complex);

    py::enum_<TETypes>(m, "TETypes", py::arithmetic())
        .value("ImagTE", TETypes::ImagTE)
        .value("RealTE", TETypes::RealTE)
        .value("TangentSpace", TETypes::TangentSpace)
        .value("RK4", TETypes::RK4)
        .value("RK4PP", TETypes::RK4PP);

    py::enum_<TruncPatternTypes>(m, "TruncPatternTypes", py::arithmetic())
        .value("Nothing", TruncPatternTypes::None)
        .value("TruncAfterOdd", TruncPatternTypes::TruncAfterOdd)
        .value("TruncAfterEven", TruncPatternTypes::TruncAfterEven);

    py::enum_<QCTypes>(m, "QCTypes", py::arithmetic())
        .value("NC", QCTypes::NC)
        .value("CN", QCTypes::CN)
        .value("NCCN", QCTypes(QCTypes::NC | QCTypes::CN))
        .value("Conventional", QCTypes::Conventional);

    py::enum_<SparseMatrixTypes>(m, "SparseMatrixTypes", py::arithmetic())
        .value("Normal", SparseMatrixTypes::Normal)
        .value("CSR", SparseMatrixTypes::CSR)
        .value("Archived", SparseMatrixTypes::Archived)
        .value("Delayed", SparseMatrixTypes::Delayed);

    py::enum_<ParallelOpTypes>(m, "ParallelOpTypes", py::arithmetic())
        .value("None", ParallelOpTypes::None)
        .value("Repeated", ParallelOpTypes::Repeated)
        .value("Number", ParallelOpTypes::Number)
        .value("Partial", ParallelOpTypes::Partial);

    py::enum_<TensorFunctionsTypes>(m, "TensorFunctionsTypes", py::arithmetic())
        .value("Normal", TensorFunctionsTypes::Normal)
        .value("Archived", TensorFunctionsTypes::Archived)
        .value("Delayed", TensorFunctionsTypes::Delayed);

    py::enum_<OperatorTensorTypes>(m, "OperatorTensorTypes", py::arithmetic())
        .value("Normal", OperatorTensorTypes::Normal)
        .value("Delayed", OperatorTensorTypes::Delayed);

    py::enum_<EquationTypes>(m, "EquationTypes", py::arithmetic())
        .value("NormalMinRes", EquationTypes::NormalMinRes)
        .value("NormalCG", EquationTypes::NormalCG)
        .value("NormalGCROT", EquationTypes::NormalGCROT)
        .value("PerturbativeCompression",
               EquationTypes::PerturbativeCompression)
        .value("GreensFunction", EquationTypes::GreensFunction)
        .value("GreensFunctionSquared", EquationTypes::GreensFunctionSquared)
        .value("FitAddition", EquationTypes::FitAddition);

    py::enum_<ConvergenceTypes>(m, "ConvergenceTypes", py::arithmetic())
        .value("LastMinimal", ConvergenceTypes::LastMinimal)
        .value("LastMaximal", ConvergenceTypes::LastMaximal)
        .value("FirstMinimal", ConvergenceTypes::FirstMinimal)
        .value("FirstMaximal", ConvergenceTypes::FirstMaximal)
        .value("MiddleSite", ConvergenceTypes::MiddleSite);

    py::enum_<TraceTypes>(m, "TraceTypes", py::arithmetic())
        .value("Nothing", TraceTypes::None)
        .value("Left", TraceTypes::Left)
        .value("Right", TraceTypes::Right);

    py::enum_<OpCachingTypes>(m, "OpCachingTypes", py::arithmetic())
        .value("Nothing", OpCachingTypes::None)
        .value("Left", OpCachingTypes::Left)
        .value("Right", OpCachingTypes::Right)
        .value("LeftCopy", OpCachingTypes::LeftCopy)
        .value("RightCopy", OpCachingTypes::RightCopy);

    py::enum_<ParallelCommTypes>(m, "ParallelCommTypes", py::arithmetic())
        .value("Nothing", ParallelCommTypes::None)
        .value("NonBlocking", ParallelCommTypes::NonBlocking)
        .def(py::self & py::self)
        .def(py::self | py::self);

    py::enum_<ParallelRulePartitionTypes>(m, "ParallelRulePartitionTypes",
                                          py::arithmetic())
        .value("Left", ParallelRulePartitionTypes::Left)
        .value("Right", ParallelRulePartitionTypes::Right)
        .value("Middle", ParallelRulePartitionTypes::Middle);

    py::enum_<ParallelTypes>(m, "ParallelTypes", py::arithmetic())
        .value("Serial", ParallelTypes::Serial)
        .value("Distributed", ParallelTypes::Distributed)
        .value("NewScheme", ParallelTypes::NewScheme)
        .def(py::self & py::self)
        .def(py::self | py::self)
        .def(py::self ^ py::self);
}

template <typename S = void> void bind_io(py::module &m) {

    m.def(
        "init_memory",
        [](size_t isize, size_t dsize, const string &save_dir,
           double dmain_ratio, double imain_ratio, int n_frames) {
            frame_() = make_shared<DataFrame>(
                isize, dsize, save_dir, dmain_ratio, imain_ratio, n_frames);
        },
        py::arg("isize") = size_t(1L << 28),
        py::arg("dsize") = size_t(1L << 30), py::arg("save_dir") = "nodex",
        py::arg("dmain_ratio") = 0.7, py::arg("imain_ratio") = 0.7,
        py::arg("n_frames") = 2);

    m.def("release_memory", []() {
        frame_()->activate(0);
        assert(ialloc_()->used == 0 && dalloc_()->used == 0);
        frame_() = nullptr;
    });

    m.def("set_mkl_num_threads", [](int n) {
#ifdef _HAS_INTEL_MKL
        mkl_set_num_threads(n);
        mkl_set_dynamic(0);
        threading_()->n_threads_mkl = n;
        threading_()->type = threading_()->type | ThreadingTypes::BatchedGEMM;
#else
        throw runtime_error("cannot set number of mkl threads.");
#endif
    });
    m.def("set_omp_num_threads", [](int n) {
#ifdef _OPENMP
        omp_set_num_threads(n);
        threading_()->n_threads_global = n;
        threading_()->type = threading_()->type | ThreadingTypes::Global;
#else
        if(n != 1)
            throw runtime_error("cannot set number of omp threads.");
#endif
    });

    m.def("read_occ", &read_occ);
    m.def("write_occ", &write_occ);

    py::class_<Allocator<uint32_t>, shared_ptr<Allocator<uint32_t>>>(
        m, "IntAllocator")
        .def(py::init<>());

    py::class_<Allocator<double>, shared_ptr<Allocator<double>>>(
        m, "DoubleAllocator")
        .def(py::init<>());

    py::class_<VectorAllocator<uint32_t>, shared_ptr<VectorAllocator<uint32_t>>,
               Allocator<uint32_t>>(m, "IntVectorAllocator")
        .def_readwrite("data", &VectorAllocator<uint32_t>::data)
        .def(py::init<>());

    py::class_<VectorAllocator<double>, shared_ptr<VectorAllocator<double>>,
               Allocator<double>>(m, "DoubleVectorAllocator")
        .def_readwrite("data", &VectorAllocator<double>::data)
        .def(py::init<>());

    py::class_<StackAllocator<uint32_t>, shared_ptr<StackAllocator<uint32_t>>,
               Allocator<uint32_t>>(m, "IntStackAllocator")
        .def(py::init<>())
        .def_readwrite("size", &StackAllocator<uint32_t>::size)
        .def_readwrite("used", &StackAllocator<uint32_t>::used)
        .def_readwrite("shift", &StackAllocator<uint32_t>::shift);

    py::class_<StackAllocator<double>, shared_ptr<StackAllocator<double>>,
               Allocator<double>>(m, "DoubleStackAllocator")
        .def(py::init<>())
        .def_readwrite("size", &StackAllocator<double>::size)
        .def_readwrite("used", &StackAllocator<double>::used)
        .def_readwrite("shift", &StackAllocator<double>::shift);

    struct Global {};

    py::class_<FPCodec<double>, shared_ptr<FPCodec<double>>>(m, "DoubleFPCodec")
        .def(py::init<double>())
        .def(py::init<double, size_t>())
        .def_readwrite("ndata", &FPCodec<double>::ndata)
        .def_readwrite("ncpsd", &FPCodec<double>::ncpsd)
        .def("encode",
             [](FPCodec<double> *self, py::array_t<double> arr) {
                 double *tmp = new double[arr.size() + 2];
                 size_t len = self->encode(arr.mutable_data(), arr.size(), tmp);
                 assert(len <= arr.size() + 2);
                 py::array_t<double> arx = py::array_t<double>(len + 1);
                 arx.mutable_data()[0] = arr.size();
                 memcpy(arx.mutable_data() + 1, tmp, len * sizeof(double));
                 delete[] tmp;
                 return arx;
             })
        .def("decode",
             [](FPCodec<double> *self, py::array_t<double> arr) {
                 size_t arr_len = arr.mutable_data()[0];
                 py::array_t<double> arx = py::array_t<double>(arr_len);
                 size_t len = self->decode(arr.mutable_data() + 1, arr_len,
                                           arx.mutable_data());
                 assert(len == arr.size() - 1);
                 return arx;
             })
        .def("write_array",
             [](FPCodec<double> *self, py::array_t<double> arr) {
                 stringstream ss;
                 self->write_array(ss, arr.mutable_data(), arr.size());
                 assert(ss.tellp() % sizeof(double) == 0);
                 size_t len = ss.tellp() / sizeof(double);
                 py::array_t<double> arx = py::array_t<double>(len + 1);
                 arx.mutable_data()[0] = arr.size();
                 ss.clear();
                 ss.seekg(0);
                 ss.read((char *)(arx.mutable_data() + 1),
                         sizeof(double) * len);
                 return arx;
             })
        .def("read_array",
             [](FPCodec<double> *self, py::array_t<double> arr) {
                 size_t arr_len = arr.mutable_data()[0];
                 stringstream ss;
                 ss.write((char *)(arr.mutable_data() + 1),
                          (arr.size() - 1) * sizeof(double));
                 py::array_t<double> arx = py::array_t<double>(arr_len);
                 ss.clear();
                 ss.seekg(0);
                 self->read_array(ss, arx.mutable_data(), arr_len);
                 return arx;
             })
        .def("save",
             [](FPCodec<double> *self, const string &filename,
                py::array_t<double> arr) {
                 ofstream ofs(filename.c_str(), ios::binary);
                 if (!ofs.good())
                     throw runtime_error("DoubleFPCodec::save on '" + filename +
                                         "' failed.");
                 ofs << arr.size();
                 self->write_array(ofs, arr.mutable_data(), arr.size());
                 if (!ofs.good())
                     throw runtime_error("DoubleFPCodec::save on '" + filename +
                                         "' failed.");
                 ofs.close();
             })
        .def("load", [](FPCodec<double> *self, const string &filename) {
            ifstream ifs(filename.c_str(), ios::binary);
            if (!ifs.good())
                throw runtime_error("DoubleFPCodec::load_data on '" + filename +
                                    "' failed.");
            size_t arr_len;
            ifs >> arr_len;
            py::array_t<double> arx = py::array_t<double>(arr_len);
            self->read_array(ifs, arx.mutable_data(), arr_len);
            if (ifs.fail() || ifs.bad())
                throw runtime_error("DoubleFPCodec::load on '" + filename +
                                    "' failed.");
            ifs.close();
            return arx;
        });

    py::class_<KuhnMunkres, shared_ptr<KuhnMunkres>>(m, "KuhnMunkres")
        .def(py::init([](const py::array_t<double> &cost) {
            assert(cost.ndim() == 2);
            const int m = (int)cost.shape()[0], n = (int)cost.shape()[1];
            const int asi = (int)cost.strides()[0] / sizeof(double),
                      asj = (int)cost.strides()[1] / sizeof(double);
            vector<double> arr(m * n);
            for (int i = 0; i < m; i++)
                for (int j = 0; j < n; j++)
                    arr[i * n + j] = cost.data()[asi * i + asj * j];
            return make_shared<KuhnMunkres>(arr, m, n);
        }))
        .def("solve", [](KuhnMunkres *self) {
            auto r = self->solve();
            py::array_t<int> idx(r.second.size());
            memcpy(idx.mutable_data(), r.second.data(),
                   r.second.size() * sizeof(int));
            return make_pair(r.first, idx);
        });

    py::class_<Prime, shared_ptr<Prime>>(m, "Prime")
        .def(py::init<>())
        .def("factors", [](Prime *self, Prime::LL n) {
            vector<pair<Prime::LL, int>> factors;
            self->factors(n, factors);
            return factors;
        });

    py::class_<FFT, shared_ptr<FFT>>(m, "FFT")
        .def(py::init<>())
        .def("init", &FFT::init)
        .def("fft",
             [](FFT *self, const py::array_t<complex<double>> &arr) {
                 py::array_t<complex<double>> arx =
                     py::array_t<complex<double>>(arr.size());
                 memcpy(arx.mutable_data(), arr.data(),
                        arr.size() * sizeof(complex<double>));
                 self->fft(arx.mutable_data(), arx.size(), true);
                 return arx;
             })
        .def("ifft",
             [](FFT *self, const py::array_t<complex<double>> &arr) {
                 py::array_t<complex<double>> arx =
                     py::array_t<complex<double>>(arr.size());
                 memcpy(arx.mutable_data(), arr.data(),
                        arr.size() * sizeof(complex<double>));
                 self->fft(arx.mutable_data(), arx.size(), false);
                 return arx;
             })
        .def_static("fftshift",
                    [](const py::array_t<complex<double>> &arr) {
                        py::array_t<complex<double>> arx =
                            py::array_t<complex<double>>(arr.size());
                        memcpy(arx.mutable_data(), arr.data(),
                               arr.size() * sizeof(complex<double>));
                        FFT::fftshift(arx.mutable_data(), arx.size(), true);
                        return arx;
                    })
        .def_static("fftshift",
                    [](const py::array_t<double> &arr) {
                        py::array_t<double> arx =
                            py::array_t<double>(arr.size());
                        memcpy(arx.mutable_data(), arr.data(),
                               arr.size() * sizeof(double));
                        FFT::fftshift(arx.mutable_data(), arx.size(), true);
                        return arx;
                    })
        .def_static("ifftshift",
                    [](const py::array_t<complex<double>> &arr) {
                        py::array_t<complex<double>> arx =
                            py::array_t<complex<double>>(arr.size());
                        memcpy(arx.mutable_data(), arr.data(),
                               arr.size() * sizeof(complex<double>));
                        FFT::fftshift(arx.mutable_data(), arx.size(), false);
                        return arx;
                    })
        .def_static("fftfreq", [](long long int n, double d) {
            py::array_t<double> arx = py::array_t<double>(n);
            FFT::fftfreq(arx.mutable_data(), n, d);
            return arx;
        });

    py::class_<DFT, shared_ptr<DFT>>(m, "DFT")
        .def(py::init<>())
        .def("init", &DFT::init)
        .def("fft",
             [](DFT *self, const py::array_t<complex<double>> &arr) {
                 py::array_t<complex<double>> arx =
                     py::array_t<complex<double>>(arr.size());
                 memcpy(arx.mutable_data(), arr.data(),
                        arr.size() * sizeof(complex<double>));
                 self->fft(arx.mutable_data(), arx.size(), true);
                 return arx;
             })
        .def("ifft", [](DFT *self, const py::array_t<complex<double>> &arr) {
            py::array_t<complex<double>> arx =
                py::array_t<complex<double>>(arr.size());
            memcpy(arx.mutable_data(), arr.data(),
                   arr.size() * sizeof(complex<double>));
            self->fft(arx.mutable_data(), arx.size(), false);
            return arx;
        });

    py::class_<DataFrame, shared_ptr<DataFrame>>(m, "DataFrame")
        .def(py::init<>())
        .def(py::init<size_t, size_t>())
        .def(py::init<size_t, size_t, const string &>())
        .def(py::init<size_t, size_t, const string &, double>())
        .def(py::init<size_t, size_t, const string &, double, double>())
        .def(py::init<size_t, size_t, const string &, double, double, int>())
        .def_readwrite("save_dir", &DataFrame::save_dir)
        .def_readwrite("mps_dir", &DataFrame::mps_dir)
        .def_readwrite("restart_dir", &DataFrame::restart_dir)
        .def_readwrite("restart_dir_per_sweep",
                       &DataFrame::restart_dir_per_sweep)
        .def_readwrite("restart_dir_optimal_mps",
                       &DataFrame::restart_dir_optimal_mps)
        .def_readwrite("restart_dir_optimal_mps_per_sweep",
                       &DataFrame::restart_dir_optimal_mps_per_sweep)
        .def_readwrite("prefix", &DataFrame::prefix)
        .def_readwrite("prefix_distri", &DataFrame::prefix_distri)
        .def_readwrite("prefix_can_write", &DataFrame::prefix_can_write)
        .def_readwrite("partition_can_write", &DataFrame::partition_can_write)
        .def_readwrite("isize", &DataFrame::isize)
        .def_readwrite("dsize", &DataFrame::dsize)
        .def_readwrite("tread", &DataFrame::tread)
        .def_readwrite("twrite", &DataFrame::twrite)
        .def_readwrite("tasync", &DataFrame::tasync)
        .def_readwrite("fpread", &DataFrame::fpread)
        .def_readwrite("fpwrite", &DataFrame::fpwrite)
        .def_readwrite("n_frames", &DataFrame::n_frames)
        .def_readwrite("i_frame", &DataFrame::i_frame)
        .def_readwrite("iallocs", &DataFrame::iallocs)
        .def_readwrite("dallocs", &DataFrame::dallocs)
        .def_readwrite("peak_used_memory", &DataFrame::peak_used_memory)
        .def_readwrite("load_buffering", &DataFrame::load_buffering)
        .def_readwrite("save_buffering", &DataFrame::save_buffering)
        .def_readwrite("use_main_stack", &DataFrame::use_main_stack)
        .def_readwrite("minimal_disk_usage", &DataFrame::minimal_disk_usage)
        .def_readwrite("fp_codec", &DataFrame::fp_codec)
        .def("update_peak_used_memory", &DataFrame::update_peak_used_memory)
        .def("reset_peak_used_memory", &DataFrame::reset_peak_used_memory)
        .def("activate", &DataFrame::activate)
        .def("load_data", &DataFrame::load_data)
        .def("save_data", &DataFrame::save_data)
        .def("reset", &DataFrame::reset)
        .def("__repr__", [](DataFrame *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });

    py::enum_<ThreadingTypes>(m, "ThreadingTypes", py::arithmetic())
        .value("SequentialGEMM", ThreadingTypes::SequentialGEMM)
        .value("BatchedGEMM", ThreadingTypes::BatchedGEMM)
        .value("Quanta", ThreadingTypes::Quanta)
        .value("QuantaBatchedGEMM", ThreadingTypes::QuantaBatchedGEMM)
        .value("Operator", ThreadingTypes::Operator)
        .value("OperatorBatchedGEMM", ThreadingTypes::OperatorBatchedGEMM)
        .value("OperatorQuanta", ThreadingTypes::OperatorQuanta)
        .value("OperatorQuantaBatchedGEMM",
               ThreadingTypes::OperatorQuantaBatchedGEMM)
        .value("Global", ThreadingTypes::Global)
        .def(py::self & py::self)
        .def(py::self ^ py::self)
        .def(py::self | py::self);

    py::class_<Threading, shared_ptr<Threading>>(m, "Threading")
        .def(py::init<>())
        .def(py::init<ThreadingTypes>())
        .def(py::init<ThreadingTypes, int>())
        .def(py::init<ThreadingTypes, int, int>())
        .def(py::init<ThreadingTypes, int, int, int>())
        .def(py::init<ThreadingTypes, int, int, int, int>())
        .def_readwrite("type", &Threading::type)
        .def_readwrite("seq_type", &Threading::seq_type)
        .def_readwrite("n_threads_op", &Threading::n_threads_op)
        .def_readwrite("n_threads_quanta", &Threading::n_threads_quanta)
        .def_readwrite("n_threads_mkl", &Threading::n_threads_mkl)
        .def_readwrite("n_threads_global", &Threading::n_threads_global)
        .def_readwrite("n_levels", &Threading::n_levels)
        .def("openmp_available", &Threading::openmp_available)
        .def("mkl_available", &Threading::mkl_available)
        .def("tbb_available", &Threading::tbb_available)
        .def("activate_global", &Threading::activate_global)
        .def("activate_normal", &Threading::activate_normal)
        .def("activate_operator", &Threading::activate_operator)
        .def("activate_quanta", &Threading::activate_quanta)
        .def("__repr__", [](Threading *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });

    py::bind_vector<vector<shared_ptr<StackAllocator<uint32_t>>>>(
        m, "VectorIntStackAllocator");
    py::bind_vector<vector<shared_ptr<StackAllocator<double>>>>(
        m, "VectorDoubleStackAllocator");

    py::class_<Global>(m, "Global")
        .def_property_static(
            "ialloc", [](py::object) { return ialloc_(); },
            [](py::object, shared_ptr<StackAllocator<uint32_t>> ia) {
                ialloc_() = ia;
            })
        .def_property_static(
            "dalloc", [](py::object) { return dalloc_(); },
            [](py::object, shared_ptr<StackAllocator<double>> da) {
                dalloc_() = da;
            })
        .def_property_static(
            "frame", [](py::object) { return frame_(); },
            [](py::object, shared_ptr<DataFrame> fr) { frame_() = fr; })
        .def_property_static(
            "threading", [](py::object) { return threading_(); },
            [](py::object, shared_ptr<Threading> th) { threading_() = th; });

    py::class_<Random, shared_ptr<Random>>(m, "Random")
        .def_static("rand_seed", &Random::rand_seed, py::arg("i") = 0U)
        .def_static("rand_int", &Random::rand_int, py::arg("a"), py::arg("b"))
        .def_static("rand_double", &Random::rand_double, py::arg("a") = 0,
                    py::arg("b") = 1)
        .def_static("fill_rand_double",
                    [](py::object, py::array_t<double> &data, double a = 0,
                       double b = 1) {
                        return Random::fill_rand_double(data.mutable_data(),
                                                        data.size(), a, b);
                    });

    py::class_<Parsing, shared_ptr<Parsing>>(m, "Parsing")
        .def_static("to_size_string", &Parsing::to_size_string,
                    py::arg("i") = (size_t)0U, py::arg("suffix") = "B");

    py::class_<ParallelProperty, shared_ptr<ParallelProperty>>(
        m, "ParallelProperty")
        .def_readwrite("owner", &ParallelProperty::owner)
        .def_readwrite("ptype", &ParallelProperty::ptype)
        .def(py::init<>())
        .def(py::init<int, ParallelOpTypes>());

#ifdef _HAS_MPI
    py::class_<block2::MPI, shared_ptr<block2::MPI>>(m, "MPI")
        .def_readwrite("_rank", &block2::MPI::_rank)
        .def_readwrite("_size", &block2::MPI::_size)
        .def(py::init<>())
        .def_static("mpi", &block2::MPI::mpi)
        .def_static("rank", &block2::MPI::rank)
        .def_static("size", &block2::MPI::size);
#endif
}

template <typename S = void> void bind_matrix(py::module &m) {
    py::class_<MatrixRef, shared_ptr<MatrixRef>>(m, "Matrix",
                                                 py::buffer_protocol())
        .def_buffer([](MatrixRef *self) -> py::buffer_info {
            return py::buffer_info(
                self->data, sizeof(double),
                py::format_descriptor<double>::format(), 2,
                {(ssize_t)self->m, (ssize_t)self->n},
                {sizeof(double) * (ssize_t)self->n, sizeof(double)});
        })
        .def_readwrite("m", &MatrixRef::m)
        .def_readwrite("n", &MatrixRef::n)
        .def("__repr__",
             [](MatrixRef *self) {
                 stringstream ss;
                 ss << *self;
                 return ss.str();
             })
        .def("allocate", &MatrixRef::allocate, py::arg("alloc") = nullptr)
        .def("deallocate", &MatrixRef::deallocate, py::arg("alloc") = nullptr);

    py::class_<ComplexMatrixRef, shared_ptr<ComplexMatrixRef>>(
        m, "ComplexMatrix", py::buffer_protocol())
        .def_buffer([](ComplexMatrixRef *self) -> py::buffer_info {
            return py::buffer_info(
                self->data, sizeof(complex<double>),
                py::format_descriptor<complex<double>>::format(), 2,
                {(ssize_t)self->m, (ssize_t)self->n},
                {sizeof(complex<double>) * (ssize_t)self->n,
                 sizeof(complex<double>)});
        })
        .def_readwrite("m", &ComplexMatrixRef::m)
        .def_readwrite("n", &ComplexMatrixRef::n)
        .def("__repr__",
             [](ComplexMatrixRef *self) {
                 stringstream ss;
                 ss << *self;
                 return ss.str();
             })
        .def("allocate", &ComplexMatrixRef::allocate,
             py::arg("alloc") = nullptr)
        .def("deallocate", &ComplexMatrixRef::deallocate,
             py::arg("alloc") = nullptr);

    py::class_<CSRMatrixRef, shared_ptr<CSRMatrixRef>>(m, "CSRMatrix")
        .def(py::init<>())
        .def(py::init<MKL_INT, MKL_INT>())
        .def_readwrite("m", &CSRMatrixRef::m)
        .def_readwrite("n", &CSRMatrixRef::n)
        .def_readwrite("nnz", &CSRMatrixRef::nnz)
        .def_property(
            "data",
            [](CSRMatrixRef *self) {
                return py::array_t<double>(self->nnz, self->data);
            },
            [](CSRMatrixRef *self, const py::array_t<double> &v) {
                assert(v.size() == self->nnz);
                memcpy(self->data, v.data(), sizeof(double) * self->nnz);
            })
        .def_property(
            "rows",
            [](CSRMatrixRef *self) {
                return py::array_t<MKL_INT>(self->m + 1, self->rows);
            },
            [](CSRMatrixRef *self, const py::array_t<MKL_INT> &v) {
                assert(v.size() == self->m + 1);
                memcpy(self->rows, v.data(), sizeof(MKL_INT) * (self->m + 1));
            })
        .def_property(
            "cols",
            [](CSRMatrixRef *self) {
                return py::array_t<MKL_INT>(self->nnz, self->cols);
            },
            [](CSRMatrixRef *self, const py::array_t<MKL_INT> &v) {
                assert(v.size() == self->nnz);
                memcpy(self->cols, v.data(), sizeof(MKL_INT) * self->nnz);
            })
        .def("__repr__",
             [](CSRMatrixRef *self) {
                 stringstream ss;
                 ss << *self;
                 return ss.str();
             })
        .def("size", &CSRMatrixRef::size)
        .def("memory_size", &CSRMatrixRef::memory_size)
        .def("transpose", &CSRMatrixRef::transpose)
        .def("sparsity", &CSRMatrixRef::sparsity)
        .def("deep_copy", &CSRMatrixRef::deep_copy)
        .def("from_dense", &CSRMatrixRef::from_dense)
        .def("to_dense", &CSRMatrixRef::to_dense)
        .def("diag", &CSRMatrixRef::diag)
        .def("trace", &CSRMatrixRef::trace)
        .def("allocate", &CSRMatrixRef::allocate)
        .def("deallocate", &CSRMatrixRef::deallocate);

    py::bind_vector<vector<shared_ptr<CSRMatrixRef>>>(m, "VectorCSRMatrix");

    py::class_<Tensor, shared_ptr<Tensor>>(m, "Tensor", py::buffer_protocol())
        .def(py::init<MKL_INT, MKL_INT, MKL_INT>())
        .def(py::init<const vector<MKL_INT> &>())
        .def_buffer([](Tensor *self) -> py::buffer_info {
            vector<ssize_t> shape, strides;
            for (auto x : self->shape)
                shape.push_back(x);
            strides.push_back(sizeof(double));
            for (int i = (int)shape.size() - 1; i > 0; i--)
                strides.push_back(strides.back() * shape[i]);
            reverse(strides.begin(), strides.end());
            return py::buffer_info(&self->data[0], sizeof(double),
                                   py::format_descriptor<double>::format(),
                                   shape.size(), shape, strides);
        })
        .def_readwrite("shape", &Tensor::shape)
        .def_readwrite("data", &Tensor::data)
        .def_property_readonly("ref", &Tensor::ref)
        .def("__repr__", [](Tensor *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });

    py::bind_vector<vector<shared_ptr<Tensor>>>(m, "VectorTensor");
    py::bind_vector<vector<vector<shared_ptr<Tensor>>>>(m,
                                                        "VectorVectorTensor");

    py::class_<MatrixFunctions>(m, "MatrixFunctions")
        .def_static("det",
                    [](py::array_t<double> &a) {
                        MKL_INT n = (MKL_INT)Prime::sqrt((Prime::LL)a.size());
                        assert(n * n == (MKL_INT)a.size());
                        return MatrixFunctions::det(
                            MatrixRef(a.mutable_data(), n, n));
                    })
        .def_static("eigs",
                    [](py::array_t<double> &a, py::array_t<double> &w) {
                        MKL_INT n = (MKL_INT)w.size();
                        MatrixFunctions::eigs(
                            MatrixRef(a.mutable_data(), n, n),
                            DiagonalMatrix(w.mutable_data(), n));
                    })
        .def_static("block_eigs", [](py::array_t<double> &a,
                                     py::array_t<double> &w,
                                     const vector<uint8_t> &x) {
            MKL_INT n = (MKL_INT)w.size();
            MatrixFunctions::block_eigs(MatrixRef(a.mutable_data(), n, n),
                                        DiagonalMatrix(w.mutable_data(), n), x);
        });

    py::class_<ComplexMatrixFunctions>(m, "ComplexMatrixFunctions");

    py::class_<CSRMatrixFunctions>(m, "CSRMatrixFunctions");

    py::class_<DiagonalMatrix, shared_ptr<DiagonalMatrix>>(
        m, "DiagonalMatrix", py::buffer_protocol())
        .def_buffer([](DiagonalMatrix *self) -> py::buffer_info {
            return py::buffer_info(self->data, sizeof(double),
                                   py::format_descriptor<double>::format(), 1,
                                   {(ssize_t)self->n}, {sizeof(double)});
        });

    py::class_<FCIDUMP, shared_ptr<FCIDUMP>>(m, "FCIDUMP")
        .def(py::init<>())
        .def("read", &FCIDUMP::read)
        .def("write", &FCIDUMP::write)
        .def("initialize_h1e",
             [](FCIDUMP *self, uint16_t n_sites, uint16_t n_elec, uint16_t twos,
                uint16_t isym, double e, const py::array_t<double> &t) {
                 self->initialize_h1e(n_sites, n_elec, twos, isym, e, t.data(),
                                      t.size());
             })
        .def("initialize_su2",
             [](FCIDUMP *self, uint16_t n_sites, uint16_t n_elec, uint16_t twos,
                uint16_t isym, double e, const py::array_t<double> &t,
                const py::array_t<double> &v) {
                 self->initialize_su2(n_sites, n_elec, twos, isym, e, t.data(),
                                      t.size(), v.data(), v.size());
             })
        .def("initialize_sz",
             [](FCIDUMP *self, uint16_t n_sites, uint16_t n_elec, uint16_t twos,
                uint16_t isym, double e, const py::tuple &t,
                const py::tuple &v) {
                 assert(t.size() == 2 && v.size() == 3);
                 py::array_t<double> ta = t[0].cast<py::array_t<double>>();
                 py::array_t<double> tb = t[1].cast<py::array_t<double>>();
                 py::array_t<double> va = v[0].cast<py::array_t<double>>();
                 py::array_t<double> vb = v[1].cast<py::array_t<double>>();
                 py::array_t<double> vab = v[2].cast<py::array_t<double>>();
                 self->initialize_sz(n_sites, n_elec, twos, isym, e, ta.data(),
                                     ta.size(), tb.data(), tb.size(), va.data(),
                                     va.size(), vb.data(), vb.size(),
                                     vab.data(), vab.size());
             })
        .def("deallocate", &FCIDUMP::deallocate)
        .def("symmetrize", &FCIDUMP::symmetrize, py::arg("orbsym"),
             "Remove integral elements that violate point group symmetry. "
             "Returns summed error in symmetrization\n\n"
             "    Args:\n"
             "        orbsym : in XOR convention")
        .def("e", &FCIDUMP::e)
        .def(
            "t",
            [](FCIDUMP *self, py::args &args) -> double {
                assert(args.size() == 2 || args.size() == 3);
                if (args.size() == 2)
                    return self->t((uint16_t)args[0].cast<int>(),
                                   (uint16_t)args[1].cast<int>());
                else
                    return self->t((uint8_t)args[0].cast<int>(),
                                   (uint16_t)args[1].cast<int>(),
                                   (uint16_t)args[2].cast<int>());
            },
            "1. (i: int, j: int) -> float\n"
            "    One-electron integral element (SU(2));\n"
            "2. (s: int, i: int, j: int) -> float\n"
            "    One-electron integral element (SZ).\n\n"
            "    Args:\n"
            "        i, j : spatial indices\n"
            "        s : spin index (0=alpha, 1=beta)")
        .def(
            "v",
            [](FCIDUMP *self, py::args &args) -> double {
                assert(args.size() == 4 || args.size() == 6);
                if (args.size() == 4)
                    return self->v((uint16_t)args[0].cast<int>(),
                                   (uint16_t)args[1].cast<int>(),
                                   (uint16_t)args[2].cast<int>(),
                                   (uint16_t)args[3].cast<int>());
                else
                    return self->v((uint8_t)args[0].cast<int>(),
                                   (uint8_t)args[1].cast<int>(),
                                   (uint16_t)args[2].cast<int>(),
                                   (uint16_t)args[3].cast<int>(),
                                   (uint16_t)args[4].cast<int>(),
                                   (uint16_t)args[5].cast<int>());
            },
            "1. (i: int, j: int, k: int, l: int) -> float\n"
            "    Two-electron integral element (SU(2));\n"
            "2. (sij: int, skl: int, i: int, j: int, k: int, l: int) -> float\n"
            "    Two-electron integral element (SZ).\n\n"
            "    Args:\n"
            "        i, j, k, l : spatial indices\n"
            "        sij, skl : spin indices (0=alpha, 1=beta)")
        .def("det_energy", &FCIDUMP::det_energy)
        .def("exchange_matrix", &FCIDUMP::exchange_matrix)
        .def("abs_exchange_matrix", &FCIDUMP::abs_exchange_matrix)
        .def("h1e_matrix", &FCIDUMP::h1e_matrix)
        .def("abs_h1e_matrix", &FCIDUMP::abs_h1e_matrix)
        .def("reorder",
             (void (FCIDUMP::*)(const vector<uint16_t> &)) & FCIDUMP::reorder)
        .def("rotate", &FCIDUMP::rotate)
        .def_static("array_reorder", &FCIDUMP::reorder<double>)
        .def_static("array_reorder", &FCIDUMP::reorder<uint8_t>)
        .def_property("orb_sym", &FCIDUMP::orb_sym, &FCIDUMP::set_orb_sym,
                      "Orbital symmetry in molpro convention")
        .def_property_readonly("n_elec", &FCIDUMP::n_elec)
        .def_property_readonly("twos", &FCIDUMP::twos)
        .def_property_readonly("isym", &FCIDUMP::isym)
        .def_property_readonly("n_sites", &FCIDUMP::n_sites)
        .def_readwrite("params", &FCIDUMP::params)
        .def_readwrite("ts", &FCIDUMP::ts)
        .def_readwrite("vs", &FCIDUMP::vs)
        .def_readwrite("vabs", &FCIDUMP::vabs)
        .def_readwrite("vgs", &FCIDUMP::vgs)
        .def_readwrite("const_e", &FCIDUMP::const_e)
        .def_readwrite("total_memory", &FCIDUMP::total_memory)
        .def_readwrite("uhf", &FCIDUMP::uhf);

    py::class_<CompressedFCIDUMP, shared_ptr<CompressedFCIDUMP>, FCIDUMP>(
        m, "CompressedFCIDUMP")
        .def(py::init<double>())
        .def(py::init<double, int>())
        .def(py::init<double, int, size_t>())
        .def("freeze", &CompressedFCIDUMP::freeze)
        .def("unfreeze", &CompressedFCIDUMP::unfreeze)
        .def_readwrite("prec", &CompressedFCIDUMP::prec)
        .def_readwrite("ncache", &CompressedFCIDUMP::ncache)
        .def_readwrite("chunk_size", &CompressedFCIDUMP::chunk_size)
        .def_readwrite("cps_ts", &CompressedFCIDUMP::cps_ts)
        .def_readwrite("cps_vs", &CompressedFCIDUMP::cps_vs)
        .def_readwrite("cps_vabs", &CompressedFCIDUMP::cps_vabs)
        .def_readwrite("cps_vgs", &CompressedFCIDUMP::cps_vgs)
        .def("initialize_su2",
             [](CompressedFCIDUMP *self, uint16_t n_sites, uint16_t n_elec,
                uint16_t twos, uint16_t isym, double e,
                const py::array_t<double> &t, const py::array_t<double> &v) {
                 stringstream st, sv;
                 st.write((char *)t.data(), sizeof(double) * t.size());
                 st.clear(), st.seekg(0);
                 sv.write((char *)v.data(), sizeof(double) * v.size());
                 sv.clear(), sv.seekg(0);
                 self->initialize_su2(n_sites, n_elec, twos, isym, e, st,
                                      t.size(), sv, v.size());
             })
        .def("initialize_su2",
             [](CompressedFCIDUMP *self, uint16_t n_sites, uint16_t n_elec,
                uint16_t twos, uint16_t isym, double e, const string &ft,
                const string &fv) {
                 ifstream ift(ft.c_str(), ios::binary);
                 ifstream ifv(fv.c_str(), ios::binary);
                 if (!ift.good())
                     throw runtime_error(
                         "CompressedFCIDUMP::initialize_su2 on '" + ft +
                         "' failed.");
                 if (!ifv.good())
                     throw runtime_error(
                         "CompressedFCIDUMP::initialize_su2 on '" + fv +
                         "' failed.");
                 size_t t_len, v_len;
                 ift >> t_len;
                 ifv >> v_len;
                 self->initialize_su2(n_sites, n_elec, twos, isym, e, ift,
                                      t_len, ifv, v_len);
                 if (ift.fail() || ift.bad())
                     throw runtime_error(
                         "CompressedFCIDUMP::initialize_su2 on '" + ft +
                         "' failed.");
                 if (ifv.fail() || ifv.bad())
                     throw runtime_error(
                         "CompressedFCIDUMP::initialize_su2 on '" + fv +
                         "' failed.");
                 ifv.close();
                 ift.close();
             })
        .def("initialize_sz", [](CompressedFCIDUMP *self, uint16_t n_sites,
                                 uint16_t n_elec, uint16_t twos, uint16_t isym,
                                 double e, const py::tuple &t,
                                 const py::tuple &v) {
            assert(t.size() == 2 && v.size() == 3);
            if (py::isinstance<py::array_t<double>>(t[0])) {
                py::array_t<double> ta = t[0].cast<py::array_t<double>>();
                py::array_t<double> tb = t[1].cast<py::array_t<double>>();
                py::array_t<double> va = v[0].cast<py::array_t<double>>();
                py::array_t<double> vb = v[1].cast<py::array_t<double>>();
                py::array_t<double> vab = v[2].cast<py::array_t<double>>();
                stringstream sta, stb, sva, svb, svab;
                sta.write((char *)ta.data(), sizeof(double) * ta.size());
                sta.clear(), sta.seekg(0);
                stb.write((char *)tb.data(), sizeof(double) * tb.size());
                stb.clear(), stb.seekg(0);
                sva.write((char *)va.data(), sizeof(double) * va.size());
                sva.clear(), sva.seekg(0);
                svb.write((char *)vb.data(), sizeof(double) * vb.size());
                svb.clear(), svb.seekg(0);
                svab.write((char *)vab.data(), sizeof(double) * vab.size());
                svab.clear(), svab.seekg(0);
                self->initialize_sz(n_sites, n_elec, twos, isym, e, sta,
                                    ta.size(), stb, tb.size(), sva, va.size(),
                                    svb, vb.size(), svab, vab.size());
            } else {
                string fta = t[0].cast<string>();
                string ftb = t[1].cast<string>();
                string fva = v[0].cast<string>();
                string fvb = v[1].cast<string>();
                string fvab = v[2].cast<string>();
                ifstream ifta(fta.c_str(), ios::binary);
                ifstream iftb(ftb.c_str(), ios::binary);
                ifstream ifva(fva.c_str(), ios::binary);
                ifstream ifvb(fvb.c_str(), ios::binary);
                ifstream ifvab(fvab.c_str(), ios::binary);
                if (!ifta.good())
                    throw runtime_error(
                        "CompressedFCIDUMP::initialize_sz on '" + fta +
                        "' failed.");
                if (!iftb.good())
                    throw runtime_error(
                        "CompressedFCIDUMP::initialize_sz on '" + ftb +
                        "' failed.");
                if (!ifva.good())
                    throw runtime_error(
                        "CompressedFCIDUMP::initialize_sz on '" + fva +
                        "' failed.");
                if (!ifvb.good())
                    throw runtime_error(
                        "CompressedFCIDUMP::initialize_sz on '" + fvb +
                        "' failed.");
                if (!ifvab.good())
                    throw runtime_error(
                        "CompressedFCIDUMP::initialize_sz on '" + fvab +
                        "' failed.");
                size_t ta_len, tb_len, va_len, vb_len, vab_len;
                ifta >> ta_len;
                iftb >> tb_len;
                ifva >> va_len;
                ifvb >> vb_len;
                ifvab >> vab_len;
                self->initialize_sz(n_sites, n_elec, twos, isym, e, ifta,
                                    ta_len, iftb, tb_len, ifva, va_len, ifvb,
                                    vb_len, ifvab, vab_len);
                if (ifta.fail() || ifta.bad())
                    throw runtime_error(
                        "CompressedFCIDUMP::initialize_sz on '" + fta +
                        "' failed.");
                if (iftb.fail() || iftb.bad())
                    throw runtime_error(
                        "CompressedFCIDUMP::initialize_sz on '" + ftb +
                        "' failed.");
                if (ifva.fail() || ifva.bad())
                    throw runtime_error(
                        "CompressedFCIDUMP::initialize_sz on '" + fva +
                        "' failed.");
                if (ifvb.fail() || ifvb.bad())
                    throw runtime_error(
                        "CompressedFCIDUMP::initialize_sz on '" + fvb +
                        "' failed.");
                if (ifvab.fail() || ifvab.bad())
                    throw runtime_error(
                        "CompressedFCIDUMP::initialize_sz on '" + fvab +
                        "' failed.");
                ifvab.close();
                ifvb.close();
                ifva.close();
                iftb.close();
                ifta.close();
            }
        });

    py::class_<OrbitalOrdering, shared_ptr<OrbitalOrdering>>(m,
                                                             "OrbitalOrdering")
        .def_static("exp_trans", &OrbitalOrdering::exp_trans, py::arg("mat"))
        .def_static("evaluate", &OrbitalOrdering::evaluate, py::arg("n_sites"),
                    py::arg("kmat"), py::arg("ord") = vector<uint16_t>())
        .def_static("fiedler", &OrbitalOrdering::fiedler, py::arg("n_sites"),
                    py::arg("kmat"))
        .def_static("ga_opt", &OrbitalOrdering::ga_opt, py::arg("n_sites"),
                    py::arg("kmat"), py::arg("n_generations") = 10000,
                    py::arg("n_configs") = 54, py::arg("n_elite") = 5,
                    py::arg("clone_rate") = 0.1, py::arg("mutate_rate") = 0.1);

    py::class_<BatchGEMMSeq, shared_ptr<BatchGEMMSeq>>(m, "BatchGEMMSeq")
        .def_readwrite("batch", &BatchGEMMSeq::batch)
        .def_readwrite("post_batch", &BatchGEMMSeq::post_batch)
        .def_readwrite("refs", &BatchGEMMSeq::refs)
        .def_readwrite("cumulative_nflop", &BatchGEMMSeq::cumulative_nflop)
        .def_readwrite("mode", &BatchGEMMSeq::mode)
        .def(py::init<>())
        .def(py::init<size_t>())
        .def(py::init<size_t, SeqTypes>())
        .def("iadd", &BatchGEMMSeq::iadd, py::arg("a"), py::arg("b"),
             py::arg("scale") = 1.0, py::arg("cfactor") = 1.0,
             py::arg("conj") = false)
        .def("multiply", &BatchGEMMSeq::multiply, py::arg("a"),
             py::arg("conja"), py::arg("b"), py::arg("conjb"), py::arg("c"),
             py::arg("scale"), py::arg("cfactor"))
        .def("rotate",
             (void (BatchGEMMSeq::*)(const MatrixRef &, const MatrixRef &,
                                     const MatrixRef &, bool, const MatrixRef &,
                                     bool, double)) &
                 BatchGEMMSeq::rotate,
             py::arg("a"), py::arg("c"), py::arg("bra"), py::arg("conj_bra"),
             py::arg("ket"), py::arg("conj_ket"), py::arg("scale"))
        .def("rotate",
             (void (BatchGEMMSeq::*)(const MatrixRef &, bool, const MatrixRef &,
                                     bool, const MatrixRef &, const MatrixRef &,
                                     double)) &
                 BatchGEMMSeq::rotate,
             py::arg("a"), py::arg("conj_a"), py::arg("c"), py::arg("conj_c"),
             py::arg("bra"), py::arg("ket"), py::arg("scale"))
        .def("tensor_product_diagonal", &BatchGEMMSeq::tensor_product_diagonal,
             py::arg("a"), py::arg("b"), py::arg("c"), py::arg("scale"))
        .def("tensor_product", &BatchGEMMSeq::tensor_product, py::arg("a"),
             py::arg("conja"), py::arg("b"), py::arg("conjb"), py::arg("c"),
             py::arg("scale"), py::arg("stride"))
        .def("divide_batch", &BatchGEMMSeq::divide_batch)
        .def("check", &BatchGEMMSeq::check)
        .def("prepare", &BatchGEMMSeq::prepare)
        .def("allocate", &BatchGEMMSeq::allocate)
        .def("deallocate", &BatchGEMMSeq::deallocate)
        .def("simple_perform", &BatchGEMMSeq::simple_perform)
        .def("auto_perform",
             (void (BatchGEMMSeq::*)(const MatrixRef &)) &
                 BatchGEMMSeq::auto_perform,
             py::arg("v") = MatrixRef(nullptr, 0, 0))
        .def("auto_perform",
             (void (BatchGEMMSeq::*)(const vector<MatrixRef> &)) &
                 BatchGEMMSeq::auto_perform,
             py::arg("vs"))
        .def("perform", &BatchGEMMSeq::perform)
        .def("clear", &BatchGEMMSeq::clear)
        .def("__call__", &BatchGEMMSeq::operator())
        .def("__repr__", [](BatchGEMMSeq *self) {
            stringstream ss;
            ss << *self;
            return ss.str();
        });
}

template <typename S = void> void bind_symmetry(py::module &m) {

    py::class_<OpNamesSet>(m, "OpNamesSet")
        .def(py::init<>())
        .def(py::init<uint32_t>())
        .def(py::init([](py::tuple names) {
            vector<OpNames> x(names.size());
            for (size_t i = 0; i < names.size(); i++)
                x[i] = names[i].cast<OpNames>();
            return OpNamesSet(x);
        }))
        .def_readwrite("data", &OpNamesSet::data)
        .def("__call__", &OpNamesSet::operator())
        .def("empty", &OpNamesSet::empty)
        .def_static("normal_ops", &OpNamesSet::normal_ops)
        .def_static("all_ops", &OpNamesSet::all_ops);

    py::class_<SiteIndex>(m, "SiteIndex")
        .def(py::init<>())
        .def(py::init<uint16_t>())
        .def(py::init<uint16_t, uint16_t, uint8_t>())
        .def(py::init([](py::tuple idxs, py::tuple sidxs) {
            vector<uint16_t> x(idxs.size());
            vector<uint8_t> sx(sidxs.size());
            for (size_t i = 0; i < idxs.size(); i++)
                x[i] = idxs[i].cast<uint16_t>();
            for (size_t i = 0; i < sidxs.size(); i++)
                sx[i] = sidxs[i].cast<uint8_t>();
            return SiteIndex(x, sx);
        }))
        .def("size", &SiteIndex::size)
        .def("spin_size", &SiteIndex::spin_size)
        .def("s", &SiteIndex::s, py::arg("i") = 0)
        .def("__getitem__",
             [](SiteIndex *self, uint8_t i) { return self->operator[](i); })
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self < py::self)
        .def("__hash__", &SiteIndex::hash)
        .def("__repr__", &SiteIndex::to_str);

    py::class_<SZ>(m, "SZ")
        .def(py::init<>())
        .def(py::init<uint32_t>())
        .def(py::init<int, int, int>())
        .def_readwrite("data", &SZ::data)
        .def_property("n", &SZ::n, &SZ::set_n)
        .def_property("twos", &SZ::twos, &SZ::set_twos)
        .def_property("pg", &SZ::pg, &SZ::set_pg)
        .def_property_readonly("multiplicity", &SZ::multiplicity)
        .def_property_readonly("is_fermion", &SZ::is_fermion)
        .def_property_readonly("count", &SZ::count)
        .def("combine", &SZ::combine)
        .def("__getitem__", &SZ::operator[])
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self < py::self)
        .def(-py::self)
        .def(py::self + py::self)
        .def(py::self - py::self)
        .def("get_ket", &SZ::get_ket)
        .def("get_bra", &SZ::get_bra, py::arg("dq"))
        .def("__hash__", &SZ::hash)
        .def("__repr__", &SZ::to_str);

    py::bind_vector<vector<SZ>>(m, "VectorSZ");

    py::class_<SU2>(m, "SU2")
        .def(py::init<>())
        .def(py::init<uint32_t>())
        .def(py::init<int, int, int>())
        .def(py::init<int, int, int, int>())
        .def_readwrite("data", &SU2::data)
        .def_property("n", &SU2::n, &SU2::set_n)
        .def_property("twos", &SU2::twos, &SU2::set_twos)
        .def_property("twos_low", &SU2::twos_low, &SU2::set_twos_low)
        .def_property("pg", &SU2::pg, &SU2::set_pg)
        .def_property_readonly("multiplicity", &SU2::multiplicity)
        .def_property_readonly("is_fermion", &SU2::is_fermion)
        .def_property_readonly("count", &SU2::count)
        .def("combine", &SU2::combine)
        .def("__getitem__", &SU2::operator[])
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self < py::self)
        .def(-py::self)
        .def(py::self + py::self)
        .def(py::self - py::self)
        .def("get_ket", &SU2::get_ket)
        .def("get_bra", &SU2::get_bra, py::arg("dq"))
        .def("__hash__", &SU2::hash)
        .def("__repr__", &SU2::to_str);

    py::bind_vector<vector<SU2>>(m, "VectorSU2");
}

#ifdef _EXPLICIT_TEMPLATE

extern template void bind_data<>(py::module &m);
extern template void bind_types<>(py::module &m);
extern template void bind_io<>(py::module &m);
extern template void bind_matrix<>(py::module &m);
extern template void bind_symmetry<>(py::module &m);

extern template void bind_expr<SZ>(py::module &m);
extern template void bind_state_info<SZ>(py::module &m, const string &name);
extern template void bind_sparse<SZ>(py::module &m);
extern template void bind_mps<SZ>(py::module &m);
extern template void bind_cg<SZ>(py::module &m);
extern template void bind_operator<SZ>(py::module &m);
extern template void bind_partition<SZ>(py::module &m);
extern template void bind_hamiltonian<SZ>(py::module &m);
extern template void bind_algorithms<SZ>(py::module &m);
extern template void bind_mpo<SZ>(py::module &m);
extern template void bind_parallel<SZ>(py::module &m);

extern template void bind_expr<SU2>(py::module &m);
extern template void bind_state_info<SU2>(py::module &m, const string &name);
extern template void bind_sparse<SU2>(py::module &m);
extern template void bind_mps<SU2>(py::module &m);
extern template void bind_cg<SU2>(py::module &m);
extern template void bind_operator<SU2>(py::module &m);
extern template void bind_partition<SU2>(py::module &m);
extern template void bind_hamiltonian<SU2>(py::module &m);
extern template void bind_algorithms<SU2>(py::module &m);
extern template void bind_mpo<SU2>(py::module &m);
extern template void bind_parallel<SU2>(py::module &m);

extern template auto bind_spin_specific<SZ>(py::module &m)
    -> decltype(typename SZ::is_sz_t());

extern template void bind_trans<SU2, SZ>(py::module &m, const string &aux_name);
extern template void bind_trans<SZ, SU2>(py::module &m, const string &aux_name);
extern template auto bind_trans_spin_specific<SU2, SZ>(py::module &m,
                                                       const string &aux_name)
    -> decltype(typename SU2::is_su2_t(typename SZ::is_sz_t()));

#endif
