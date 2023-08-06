use numpy::PyArray2;
use pyo3::exceptions::{PyIndexError, PyKeyError, PyTypeError};
use pyo3::prelude::*;
use pyo3::PyObjectProtocol;
use pyo3::{PyErr, PyResult};
use std::fmt;

struct AxialErrorWrap {
    error: rustycoils::AxialError,
}
impl std::convert::From<rustycoils::AxialError> for AxialErrorWrap {
    fn from(err: rustycoils::AxialError) -> AxialErrorWrap {
        AxialErrorWrap { error: err }
    }
}
impl std::fmt::Display for AxialErrorWrap {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.error.to_string())
    }
}
impl std::convert::From<AxialErrorWrap> for PyErr {
    fn from(err: AxialErrorWrap) -> PyErr {
        match err.error {
            rustycoils::AxialError::KeyMissingError(_) => {
                PyKeyError::new_err(err.error.to_string())
            }
            rustycoils::AxialError::KeyDuplicateError(_) => {
                PyKeyError::new_err(err.error.to_string())
            }
            rustycoils::AxialError::IncompatiblePrimitiveError(_, _) => {
                PyTypeError::new_err(err.error.to_string())
            }
            rustycoils::AxialError::ReservedWordError(_) => {
                PyKeyError::new_err(err.error.to_string())
            }
        }
    }
}

#[pymodule]
fn rustpycoils(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<AxialSystemWrapper>()?;
    Ok(())
}

#[pyclass(name = "AxialSystem", module = "rustycoils_py")]
struct AxialSystemWrapper {
    axialsystem: rustycoils::AxialSystem,
}
#[pymethods]
impl AxialSystemWrapper {
    #[new]
    fn new() -> Self {
        AxialSystemWrapper {
            axialsystem: rustycoils::AxialSystem::default(),
        }
    }
    pub fn transform_x(&mut self) -> PyResult<()> {
        self.axialsystem.transform_x();
        Ok(())
    }
    pub fn transform_y(&mut self) -> PyResult<()> {
        self.axialsystem.transform_y();
        Ok(())
    }
    pub fn transform_z(&mut self) -> PyResult<()> {
        self.axialsystem.transform_z();
        Ok(())
    }
    pub fn add_loop(
        &mut self,
        id: String,
        radius: f64,
        position: f64,
        current: f64,
    ) -> PyResult<()> {
        let res = match self.axialsystem.add_loop(id, radius, position, current) {
            Ok(_) => Ok(()),
            Err(e) => Err(AxialErrorWrap::from(e)),
        };
        Ok(res?)
    }
    pub fn add_annular(
        &mut self,
        id: String,
        radius: f64,
        thickness: f64,
        position: f64,
        current: f64,
    ) -> PyResult<()> {
        let res = match self
            .axialsystem
            .add_annular(id, radius, thickness, position, current)
        {
            Ok(_) => Ok(()),
            Err(e) => Err(AxialErrorWrap::from(e)),
        };
        Ok(res?)
    }
    pub fn add_solenoid(
        &mut self,
        id: String,
        radius: f64,
        length: f64,
        position: f64,
        current: f64,
    ) -> PyResult<()> {
        let res = match self
            .axialsystem
            .add_thin_solenoid(id, radius, length, position, current)
        {
            Ok(_) => Ok(()),
            Err(e) => Err(AxialErrorWrap::from(e)),
        };
        Ok(res?)
    }
    pub fn add_coil(
        &mut self,
        id: String,
        radius: f64,
        thickness: f64,
        length: f64,
        position: f64,
        current: f64,
    ) -> PyResult<()> {
        let res = match self
            .axialsystem
            .add_coil_solenoid(id, radius, thickness, length, position, current)
        {
            Ok(_) => Ok(()),
            Err(e) => Err(AxialErrorWrap::from(e)),
        };
        Ok(res?)
    }
    pub fn modify_radius(&mut self, id: &str, radius: f64) -> PyResult<()> {
        let res = match self.axialsystem.modify_radius(id, radius) {
            Ok(_) => Ok(()),
            Err(e) => Err(AxialErrorWrap::from(e)),
        };
        Ok(res?)
    }
    pub fn modify_current(&mut self, id: &str, current: f64) -> PyResult<()> {
        let res = match self.axialsystem.modify_current(id, current) {
            Ok(_) => Ok(()),
            Err(e) => Err(AxialErrorWrap::from(e)),
        };
        Ok(res?)
    }
    pub fn modify_thickness(&mut self, id: &str, thickness: f64) -> PyResult<()> {
        let res = match self.axialsystem.modify_thickness(id, thickness) {
            Ok(_) => Ok(()),
            Err(e) => Err(AxialErrorWrap::from(e)),
        };
        Ok(res?)
    }
    pub fn modify_length(&mut self, id: &str, length: f64) -> PyResult<()> {
        let res = match self.axialsystem.modify_length(id, length) {
            Ok(_) => Ok(()),
            Err(e) => Err(AxialErrorWrap::from(e)),
        };
        Ok(res?)
    }
    pub fn modify_position(&mut self, id: &str, position: f64) -> PyResult<()> {
        let res = match self.axialsystem.modify_position(id, position) {
            Ok(_) => Ok(()),
            Err(e) => Err(AxialErrorWrap::from(e)),
        };
        Ok(res?)
    }
    pub fn get_field(&self, coordinates: [f64; 3], tol: f64) -> PyResult<Vec<f64>> {
        let [x, y, z] = self.axialsystem.get_field(coordinates, &tol);
        Ok(vec![x, y, z])
    }
    pub fn get_field_axial(&mut self, z: f64, r: f64, tol: f64) -> PyResult<Vec<f64>> {
        let [z, r] = self.axialsystem.get_field_axial(&[z, r], &tol);
        Ok(vec![z, r])
    }

    pub fn view(&self, id: &str) -> PyResult<String> {
        let i = self.axialsystem.view(id);
        let res = match i {
            Ok(string) => Ok(string),
            Err(e) => Err(AxialErrorWrap::from(e)),
        };
        Ok(res?)
    }
    /// Computes the magnetic field vector for the given position.
    ///
    /// This function makes use of a Rayon accelerated parallel iterator in the ndarray crate.
    ///
    /// # Arguments
    ///  `positions` a list containing 3D coordinates for evaluation
    ///  `tol` - the tolerance at which to stop including expansion terms
    ///  ```
    pub fn get_b(&self, positions: &PyArray2<f64>, tol: f64) -> PyResult<Py<PyArray2<f64>>> {
        let fields =
            rustycoils::get_b_ndarray(&self.axialsystem, unsafe { &positions.as_array() }, tol);
        let fields = match fields {
            Ok(fields) => fields,
            Err(_) => {
                return Err(PyIndexError::new_err(
                    "failed to convert input array into correct shape".to_string(),
                ))
            }
        };
        //let convert = fields;
        let gil = pyo3::Python::acquire_gil();
        let b_result_array = PyArray2::from_array(gil.python(), &fields);
        Ok(b_result_array.to_owned())
    }
}

#[pyproto]
impl PyObjectProtocol for AxialSystemWrapper {
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("{}", self.axialsystem))
    }
}
