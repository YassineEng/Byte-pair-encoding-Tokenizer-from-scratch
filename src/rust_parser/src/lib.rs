use pyo3::prelude::*;
use std::collections::HashMap;

#[pyclass]
#[derive(Clone, Debug)]
struct UnicodeChar {
    #[pyo3(get)]
    code_point: u32,
    #[pyo3(get)]
    name: String,
    #[pyo3(get)]
    category: String,
    #[pyo3(get)]
    combining: u8,
    #[pyo3(get)]
    bidirectional: String,
    #[pyo3(get)]
    decomposition: String,
    #[pyo3(get)]
    decimal: Option<u32>,
    #[pyo3(get)]
    digit: Option<u32>,
    #[pyo3(get)]
    numeric: Option<String>,
    #[pyo3(get)]
    mirrored: String,
    #[pyo3(get)]
    unicode1_name: String,
    #[pyo3(get)]
    iso_comment: String,
    #[pyo3(get)]
    uppercase: Option<u32>,
    #[pyo3(get)]
    lowercase: Option<u32>,
    #[pyo3(get)]
    titlecase: Option<u32>,
}

#[pyfunction]
fn parse_unicode_data(py: Python, filename: &str) -> PyResult<HashMap<u32, Py<UnicodeChar>>> {
    let allowed_ranges: Vec<(u32, u32)> = vec![
        (0x0000, 0x007F + 1),
        (0x0080, 0x00FF + 1),
        (0x2000, 0x206F + 1),
        (0x20A0, 0x20CF + 1),
        (0x2100, 0x214F + 1),
        (0x2200, 0x22FF + 1),
        (0xFB00, 0xFB4F + 1),
    ];

    let is_allowed = |cp: u32| {
        allowed_ranges.iter().any(|(start, end)| cp >= *start && cp <= *end)
    };

    let mut chars = HashMap::new();
    let content = std::fs::read_to_string(filename).expect("Could not read file");

    for line in content.lines() {
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let fields: Vec<&str> = line.split(';').collect();
        if fields.len() != 15 {
            continue;
        }

        let code_point = u32::from_str_radix(fields[0], 16).unwrap();
        if !is_allowed(code_point) {
            continue;
        }

        let char = UnicodeChar {
            code_point,
            name: fields[1].to_string(),
            category: fields[2].to_string(),
            combining: fields[3].parse().unwrap_or(0),
            bidirectional: fields[4].to_string(),
            decomposition: fields[5].to_string(),
            decimal: fields[6].parse().ok(),
            digit: fields[7].parse().ok(),
            numeric: if fields[8].is_empty() { None } else { Some(fields[8].to_string()) },
            mirrored: fields[9].to_string(),
            unicode1_name: fields[10].to_string(),
            iso_comment: fields[11].to_string(),
            uppercase: u32::from_str_radix(fields[12], 16).ok(),
            lowercase: u32::from_str_radix(fields[13], 16).ok(),
            titlecase: u32::from_str_radix(fields[14], 16).ok(),
        };
        chars.insert(code_point, Py::new(py, char).unwrap());
    }
    Ok(chars)
}

#[pymodule]
fn rust_parser(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_unicode_data, m)?)?;
    m.add_class::<UnicodeChar>()?;
    Ok(())
}