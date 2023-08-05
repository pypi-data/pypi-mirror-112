/*! \file variant.hpp
    \brief Support for std::variant
    \ingroup STLSupport */
/*
  Copyright (c) 2014, 2017, Randolph Voorhies, Shane Grant, Juan Pedro
  Bolivar Puente. All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:
      * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
      * Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
      * Neither the name of cereal nor the
        names of its contributors may be used to endorse or promote products
        derived from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL RANDOLPH VOORHIES OR SHANE GRANT BE LIABLE FOR ANY
  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
#ifndef TIMEMORY_CEREAL_TYPES_STD_VARIANT_HPP_
#define TIMEMORY_CEREAL_TYPES_STD_VARIANT_HPP_

#include "timemory/tpls/cereal/cereal/cereal.hpp"
#include <cstdint>
#include <variant>

namespace tim
{
namespace cereal
{
namespace variant_detail
{
//! @internal
template <class Archive>
struct variant_save_visitor
{
    variant_save_visitor(Archive& ar_)
    : ar(ar_)
    {}

    template <class T>
    void operator()(T const& value) const
    {
        ar(TIMEMORY_CEREAL_NVP_("data", value));
    }

    Archive& ar;
};

//! @internal
template <int N, class Variant, class... Args, class Archive>
typename std::enable_if<N == std::variant_size_v<Variant>, void>::type
load_variant(Archive& /*ar*/, int /*target*/, Variant& /*variant*/)
{
    throw ::tim::cereal::Exception("Error traversing variant during load");
}
//! @internal
template <int N, class Variant, class H, class... T, class Archive>
    typename std::enable_if < N<std::variant_size_v<Variant>, void>::type
                              load_variant(Archive& ar, int target, Variant& variant)
{
    if(N == target)
    {
        H value;
        ar(TIMEMORY_CEREAL_NVP_("data", value));
        variant = std::move(value);
    }
    else
        load_variant<N + 1, Variant, T...>(ar, target, variant);
}

}  // namespace variant_detail

//! Saving for std::variant
template <class Archive, typename VariantType1, typename... VariantTypes>
inline void
TIMEMORY_CEREAL_SAVE_FUNCTION_NAME(
    Archive& ar, std::variant<VariantType1, VariantTypes...> const& variant)
{
    std::int32_t index = static_cast<std::int32_t>(variant.index());
    ar(TIMEMORY_CEREAL_NVP_("index", index));
    variant_detail::variant_save_visitor<Archive> visitor(ar);
    std::visit(visitor, variant);
}

//! Loading for std::variant
template <class Archive, typename... VariantTypes>
inline void
TIMEMORY_CEREAL_LOAD_FUNCTION_NAME(Archive& ar, std::variant<VariantTypes...>& variant)
{
    using variant_t = typename std::variant<VariantTypes...>;

    std::int32_t index;
    ar(TIMEMORY_CEREAL_NVP_("index", index));
    if(index >= static_cast<std::int32_t>(std::variant_size_v<variant_t>))
        throw Exception("Invalid 'index' selector when deserializing std::variant");

    variant_detail::load_variant<0, variant_t, VariantTypes...>(ar, index, variant);
}

//! Serializing a std::monostate
template <class Archive>
void
TIMEMORY_CEREAL_SERIALIZE_FUNCTION_NAME(Archive&, std::monostate const&)
{}
}  // namespace cereal
}  // namespace tim

#endif  // TIMEMORY_CEREAL_TYPES_STD_VARIANT_HPP_
