/// Wrap each of the interface functions of runwrap.

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use runwrap;

#[pyfunction]
fn wrap(raw: &str, width: usize) -> PyResult<String> {
    Ok(runwrap::wrap(raw, width))
}
#[pyfunction]
fn rewrap(raw: &str, width: usize) -> PyResult<String> {
    Ok(runwrap::rewrap(raw, width))
}
#[pyfunction]
fn unwrap(raw: &str) -> PyResult<String> {
    Ok(runwrap::unwrap(raw))
}

/// Expose a Python module implemented in Rust.
#[pymodule]
fn punwrap(_: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(wrap, m)?)?;
    m.add_function(wrap_pyfunction!(rewrap, m)?)?;
    m.add_function(wrap_pyfunction!(unwrap, m)?)?;

    Ok(())
}
