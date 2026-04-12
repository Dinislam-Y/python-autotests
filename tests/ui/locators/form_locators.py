class FormLocators:
    """Форма записи на занятия — живёт внутри модалки #modal-order-new."""
    # кнопка, открывающая модалку с формой
    # playwright не умеет мешать css и text= в одном селекторе, поэтому только css
    OPEN_MODAL_BUTTON = "a[href='#modal-order-new']"
    # сама форма внутри модалки
    # модалка может быть и form.pre_n_form и просто .pre_n_form или #modal-order-new
    FORM_CONTAINER = "#modal-order-new"
    CLASS_SELECT = "#modal-order-new select"
    # опции внутри селекта классов (кроме placeholder-а)
    CLASS_SELECT_OPTIONS = "#modal-order-new select option:not([value=''])"
    PHONE_INPUT = "#modal-order-new [data-phone-pattern], #modal-order-new input[type='tel']"
    CONSENT_CHECKBOX = "#modal-order-new input[type='checkbox']"
    SUBMIT_BUTTON = "#modal-order-new .btn-warning"
    # оверлей модалки — клик по нему закрывает форму
    MODAL_OVERLAY = "#modal-order-new .modal__overlay, #modal-order-new .overlay, .modal-overlay"
