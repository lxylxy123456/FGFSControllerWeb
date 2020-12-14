//
// FGFSControllerWeb - Using an iOS Device to Control FGFS
// Copyright (C) 2020  Eric Li 李宵逸
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

// Vector library

const vi = [1.0, 0.0, 0.0];	// x 单位向量(相对手机固定)，很少平行地面
const vj = [0.0, 1.0, 0.0];	// y 单位向量(相对手机固定)，很少垂直地面
const vk = [0.0, 0.0, 1.0];	// z 单位向量(相对手机固定)

function v_neg(a) {
	return [-a[0], -a[1], -a[2]];
}

function v_times(a, b) {
	// Scalar multiplication
	return [a[0] * b, a[1] * b, a[2] * b];
}

function v_plus(a, b) {
	return [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
}

function v_minus(a, b) {
	return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
}

function v_dot(a, b) {
	return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

function v_cross(a, b) {
	return [a[1] * b[2] - a[2] * b[1],
			a[2] * b[0] - a[0] * b[2],
			a[0] * b[1] - a[1] * b[0]];
}

function v_abs(a) {
	// Vector length
	return Math.sqrt(v_dot(a, a));
}

function v_hat(a) {
	// Normalize
	return v_times(a, 1.0 / v_abs(a));
}

function v_proj(a, n) {
	// 将向量 a 投影到和 n 垂直的平面上
	// a_vec - n_vec * ((n_vec * a_vec) / (n_vec * n_vec))
	return v_minus(a, v_times(n, v_dot(n, a) / v_dot(n, n)))
}

function v_angle(a, b, c) {
	// 从 a 到 b 按 c 进行右手定则旋转的角度，返回 [-Math.PI, Math.PI)
	let angle = Math.acos(v_dot(a, b) / v_abs(a) / v_abs(b))
	if (v_dot(v_cross(a, b), c) > 0) {
		return angle;
	}
	else {
		return -angle;
	}
}

function rel_angle(a, b) {
	// a 转到 b 的相对角度，返回 [-Math.PI, Math.PI)
	let answer = b - a;
	while (answer >= Math.PI) {
		answer -= 2 * Math.PI;
	}
	while (answer < -Math.PI) {
		answer += 2 * Math.PI;
	}
	return answer;
}
